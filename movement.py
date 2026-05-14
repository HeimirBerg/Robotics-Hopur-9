"""
Hreyfing / Movement Module

Allar skipanir til að senda hraða á mótorana sem keyra róbótann.
"""

import smbus # type: ignore
import time


I2C_ADDRESS   = 0x50  # Arduino slave address
DATA_REGISTER = 0x00  # Pi address to write data too
bus = smbus.SMBus(1)  # I2C bus on Pi Zero / Pi 3 / Pi 4


MIN_VELOCITY: int = -255
MAX_VELOCITY: int =  255
MIN_SPEED: int    =   15  # Minnsti hraði sem er hægt að senda á mótora
MAX_SPEED: int    =  255  # Mesti hraði sem er hægt að senda á mótora
MIN_TURN: int     =   -1  # Minnsta beygja sem er hægt að taka
MAX_TURN: int     =    3  # Mesta beygja sem er hægt að taka


def send_speeds(m1: int, m2: int) -> str:
    """
    Sendir hraða og stefnu á mótora.
    Formerki á `m2_sign` er öfugt til að leiðrétta snúningsátt.
    
    :m1: Mótor 1, bil er [-255 til 255].
    :m2: Mótor 2, bil er [-255 til 255].
    """
    
    m1 = int(m1)
    m2 = int(m2)

    if not ((MIN_VELOCITY <= m1 <= MAX_VELOCITY) and (MIN_VELOCITY <= m2 <= MAX_VELOCITY)):
        raise ValueError("Ógilt bil")
    
    # Skipti inntaki í stærð + formerki
    m1_speed = abs(m1)
    m1_sign = 0 if m1 >= 0 else 1

    m2_speed = abs(m2)
    m2_sign = 1 if m2 >= 0 else 0 # Leiðrétt formerki

    # Pakka gögnum í 4 bytes [speed1, sign1, speed2, sign2]
    data = [m1_speed, m1_sign, m2_speed, m2_sign]

    # Sendi gögn á MCU með I2C
    bus.write_i2c_block_data(I2C_ADDRESS, DATA_REGISTER, data)
    
    return f"Hraðar sendir -> Mótor 1: {m1}, Mótor 2: {-m2}."


def forward(speed: int) -> None:
    """Keyrir áfram"""
    vel = int(speed)
    send_speeds(vel, vel)


def reverse(speed: int) -> None:
    """Bakkar"""
    vel = int(speed)
    send_speeds(-vel, -vel)


def turn(direction: str, speed: int, turn_speed: int) -> None:
    """
    Beygjir í valda átt.
    
    :direction: Settja inn `"Hægri"` eða `"Vinstri"`.
    :speed: Óbreyttur hraði, hraðinn á hjóli utan í beygju.
    :turn_speed: Hraðinn á hjóli inn í beygju.
    """
    vel = int(speed)
    turn_vel = int(turn_speed)

    if direction == "Hægri":
        send_speeds(vel, turn_vel)
    elif direction == "Vinstri":
        send_speeds(turn_vel, vel)
    else:
        raise ValueError("Ógild átt valinn, sláðu inn \"Hægri\" eða \"Vinstri\".")


def stop() -> str:
    """Stoppar mótora"""
    send_speeds(0,0)
    return "Stoppaði mótora."


def drive(speed: int, direction: int, turn_stage: int = 0) -> None:
    """
    Sameinað keyrslu fall. Ákveður hvaða hraða á að senda á mótora, stefnu og beygju virkni.

    :speed: Bil er [15 til 255].
    :direction: `1` = Áfram, `2` = Bakka, `3` = Vinstri `4` = Hægri.
    :turn_stage: `-1` = Á staðnum; `0` = Full; `1` = Skref 1; `2` = Skref 2; `3` = Aflíðandi.
    """

    m1: int = 0          # Hraði og stefna sent á Mótor 1
    m2: int = 0          # Hraði og stefna sent á Mótor 2
    turn_speed: int = 0  # Hraði hjóls inn í beygju

    try:
        speed = int(speed)
        direction = int(direction)
        turn_stage = int(turn_stage)

        if not (MIN_SPEED <= speed <= MAX_SPEED):
            print("Ógildur hraði. Bil er [15 til 255].")
            return
            
        # Reikna hraða hjóls inn í beygju
        if turn_stage == -1:
            turn_speed = -speed
        elif turn_stage == 0:
            turn_speed = 0
        elif turn_stage == 1:
            turn_speed = int(speed/2.5)
        elif turn_stage == 2:
            turn_speed = int(speed/1.9)
        elif turn_stage == 3:
            turn_speed = int(speed/1.3)
        else:
            turn_speed = 0
            print("Ógilt beygju skref valið, nota 0 sem sjálfgefið.")

        # Ákveð gildin sem á að senda á mótora
        if direction == 1:   # Áfram
            m1 = speed
            m2 = speed
        elif direction == 2: # Bakka
            m1 = -speed
            m2 = -speed
        elif direction == 3: # Vinstri
            m1 = turn_speed
            m2 = speed
        elif direction == 4: # Hægri
            m1 = speed
            m2 = turn_speed
        else:
            print(stop())
            print("Ógild átt er valin! Valmöguleikar eru 1 til 4.")
            return
        
        # Sendi hraðana á mótora
        send_speeds(m1,m2)
        
    except ValueError:
        print(stop())
        print("Ógild tala slegin inn, sláðu inn heiltölu.")
        return
    
    return


def get_new_speed() -> int:
    """Spyr notanda um nýjann hraða."""

    speed: int | None = None
    
    while speed is None:
        try:
            speed = int(input("Veldu nýjann hraða á bilinu [15 til 255]: "))

            if not (MIN_SPEED <= speed <= MAX_SPEED):
                raise ValueError
    
        except ValueError:
            speed = None
            print(f"Ógildur hraði sleginn inn.")
    
    return speed


def get_new_turn_stage() -> int:
    """Spyr notanda um nýtt beygju skref."""

    turn: int | None = None

    while turn is None:
        try:
            turn = int(input("Veldu nýtt beygju skref á bilinu [-1 til 3]: "))

            if not (MIN_TURN <= turn <= MAX_TURN):
                raise ValueError
        
        except ValueError:
            turn = None
            print(f"Ógilt beygju skref valið.")

    return turn


def calculate_boosts(
        reference_time: float, 
        init_speed: int, 
        init_turn: int, 
        speed_boost: int,
        wait_times: tuple[int, int]
        ) -> tuple[int, int]:
    """
    Reiknar aukinn hraða og beygju hraða eftir ákveðna seinkun.
    
    :reference_time: Viðmiðunar tími í reikningum.
    :init_speed: Upphafs hraði.
    :init_turn: Upphafs beygju stig.
    :speed_boost: Hraðinn sem er bætt bið eftir biðtímann.
    :wait_times: Biðtímar í túplu, tuple[styttri tími, lengri tími].
    :return: Útreiknaður hraði og beygju skref í túplu.
    """

    # Hjálpar fall til að losna við if setningar
    def clamp(low, value, high):
        """Klemmir gildi á milli `low` (MIN) og `high` (MAX)."""
        return max(low, min(value, high))

    # Tími liðinn frá því fyrsta takka var ýtt niður.
    elapsed_time: float = time.time() - reference_time

    if elapsed_time >= wait_times[1]:
        speed = clamp(MIN_SPEED, (init_speed + (speed_boost * 2)), MAX_SPEED)
        turn = clamp(MIN_TURN, (init_turn + 2), MAX_TURN)

    elif elapsed_time >= wait_times[0]:
        speed = clamp(MIN_SPEED, (init_speed + speed_boost), MAX_SPEED)
        turn = clamp(MIN_TURN, (init_turn + 1), MAX_TURN)

    else:
        speed = init_speed
        turn = init_turn

    return speed, turn


def auto_calculate_turn(direction, distance, speed):
    turn_speed = int(speed * (distance - 60) / 80)
    turn_speed = max(0, min(turn_speed, speed))
    return turn(direction, speed, turn_speed)




# ------------------------------------------------------------------ 

# // def senda(m1,m2):
# //    m1 = int(m1)
# //    m2 = int(m2)
# //     m1_sign  = 0 if m1 >= 0 else 1
# //     m2_sign  = 0 if m2 >= 0 else 1
# //     m1_speed = abs(m1)
# //     m2_speed = abs(m2)
# //     data = [m1_speed, m1_sign, m2_speed, m2_sign]
# //     bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)
# //     return f"Sent speeds → Motor1: {m1}, Motor2: {m2}"

# def fara_afram(hradi):
#     hradi = int(hradi)
#     return senda(hradi,-hradi)
    
# def fara_aftur(hradi):
#     hradi = int(hradi)
#     return senda(-hradi,hradi)

# def beygja(att, m1, m2):
#     m1 = int(m1)
#     m2 = int(m2)

#     if att == "Hægri":
#         return send_speeds(m1, -m2)

#     elif att == "Vinstri":
#         return send_speeds(m2, -m1)
#     else:
#         return "Villa! skrifaðu annað hvort \"Hægri\" eða \"Vinstri\""
    

# def stoppa():
#     return senda(0,0)








# def velja_hrada():
#     while True:
#         try:
#             hradi = int(input("Veldu hraða [15-255]: "))

#             if not (15 <= hradi <= 255):
#                 print("Ógilt val! Sláðu inn heiltölu á bilinu [15-255].")
#                 continue
#             else:
#                 break

#         except ValueError:
#             print("Ógilt val! Sláðu inn heiltölu á bilinu [15-255].")
#             continue

#     return hradi

# def velja_radius(hradi):

#     hradi = int(hradi)

#     print(" Veldu hversu krappa beygju á að taka:\n 1: Á staðnum\n 2: Kröpp\n 3: Milli-millistig\n 4: Millistig\n 5: Aflíðandi")

#     while True:
#         try:
#             val = int(input("Val: "))

#             if val == 1:
#                 radius = -hradi
#                 break
#             elif val == 2:
#                 radius = 0
#                 break
#             elif val == 3:
#                 radius = (hradi/2.5)
#                 break
#             elif val == 4:
#                 radius = (hradi/1.9)
#                 break
#             elif val == 5:
#                 radius = (hradi/1.3)
#                 break
#             else:
#                 print("Ógilt val!")
#                 continue

#         except ValueError:
#             print("Ógilt val!")
#             continue

#     radius = int(radius)
#     return radius


    
    



