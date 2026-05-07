import smbus # type: ignore
I2C_ADDRESS = 0x50   # Arduino slave address
bus = smbus.SMBus(1) # I2C bus on Pi Zero / Pi 3 / Pi 4

from config import Speed, Velocity, TurnStage

def senda(m1,m2):
    m1 = int(m1)
    m2 = int(m2)
    m1_sign  = 0 if m1 >= 0 else 1
    m2_sign  = 0 if m2 >= 0 else 1
    m1_speed = abs(m1)
    m2_speed = abs(m2)
    data = [m1_speed, m1_sign, m2_speed, m2_sign]
    bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)
    return f"Sent speeds → Motor1: {m1}, Motor2: {m2}"

def fara_afram(hradi):
    hradi = int(hradi)
    return senda(hradi,-hradi)
    
def fara_aftur(hradi):
    hradi = int(hradi)
    return senda(-hradi,hradi)

def beygja(att, m1, m2):
    m1 = int(m1)
    m2 = int(m2)

    if att == "Hægri":
        return senda(m1, -m2)

    elif att == "Vinstri":
        return senda(m2, -m1)
    else:
        return "Villa! skrifaðu annað hvort \"Hægri\" eða \"Vinstri\""
def stoppa():
    return senda(0,0)

def velja_hrada():
    while True:
        try:
            hradi = int(input("Veldu hraða [15-255]: "))

            if not (15 <= hradi <= 255):
                print("Ógilt val! Sláðu inn heiltölu á bilinu [15-255].")
                continue
            else:
                break

        except ValueError:
            print("Ógilt val! Sláðu inn heiltölu á bilinu [15-255].")
            continue

    return hradi

def velja_radius(hradi):

    hradi = int(hradi)

    print(" Veldu hversu krappa beygju á að taka:\n 1: Á staðnum\n 2: Kröpp\n 3: Milli-millistig\n 4: Millistig\n 5: Aflíðandi")

    while True:
        try:
            val = int(input("Val: "))

            if val == 1:
                radius = -hradi
                break
            elif val == 2:
                radius = 0
                break
            elif val == 3:
                radius = (hradi/2.5)
                break
            elif val == 4:
                radius = (hradi/1.9)
                break
            elif val == 5:
                radius = (hradi/1.3)
                break
            else:
                print("Ógilt val!")
                continue

        except ValueError:
            print("Ógilt val!")
            continue

    radius = int(radius)
    return radius

def reikna_beygju(direction, distance, hradi):
    radius = int(hradi * (distance - 20) / 80)
    radius = max(0, radius)
    return beygja(direction, hradi, radius)
    
    



# -------------------- ------------------ --------------------- #
# -------------------- Gunnar, Prufu kóði --------------------- #
# -------------------- ------------------ --------------------- #


DATA_REGISTER = 0x00  # Pi address to write data to


def send_speeds(m1: Velocity | int, m2: Velocity | int) -> str:
    """
    Sends velocity values to each motor. Corrects sign on inverted Motor 2
    
    `m1` and `m2` range -255 to 255.
    """
    
    try:
        # Check if inputs are integers
        m1 = Velocity(m1)
        m2 = Velocity(m2)

        # // # Validate range
        # // if not ((-255 <= m1 <= 255) and (-255 <= m2 <= 255)):
        # //    return "Requested speeds not in range -255 to 255."
        
        # Split input into magnitude + sign
        m1_speed = abs(m1)
        m1_sign = 0 if m1 >= 0 else 1

        m2_speed = abs(m2)
        m2_sign = 1 if m2 >= 0 else 0 # Inverted sign to correct direction of rotation

        # Pack data into 4 bytes [speed1, sign1, speed2, sign2]
        data = [m1_speed, m1_sign, m2_speed, m2_sign]

        # Send data to MCU via I2C
        bus.write_i2c_block_data(I2C_ADDRESS, DATA_REGISTER, data)

    except ValueError:
        return "Invalid number."
    
    return f"Speeds sent -> Motor 1: {m1}, Motor 2: {-m2}."
    

def stop() -> str:
    """Stops motors"""
    send_speeds(0,0)
    return "Motors stopped"


def drive(speed: Speed | int, direction: int, turn_stage: TurnStage | int = 0) -> None:
    """
    Combined driving functions. Includes speed assignment to each motor, direction and turning logic.

    :speed: Range `15 - 255`.
    :direction: `1` = Forward; `2` = Reverse; `3` = Turn left; `4` = Turn right.
    :turn_stage: `-1` = On Spot; `0` = Full; `1` = Stage 1; `2` = Stage 2; `3` = Shallow.
    """

    # Setup
    # m1 = Velocity(0)     # Velocity sent to Motor 1
    # m2 = Velocity(0)     # Velocity sent to Motor 2
    turn_speed: int = 0  # Speed of the wheel inside turn

    try:
        # Check if inputs are integers
        speed = Speed(speed)
        direction = int(direction)
        turn_stage = TurnStage(turn_stage)

        # Range check inputs
        # if not (15 <= speed <= 255):
        #     print("Invalid speed entered! Range is 15-255.")
        #     return
            
        # Calculate speed of wheel inside turn
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

        # Assign velocity values sent to each motor
        if direction == 1:   # Forward
            m1 = Velocity(speed)
            m2 = Velocity(speed)
        elif direction == 2: # Reverse
            m1 = Velocity(-speed)
            m2 = Velocity(-speed)
        elif direction == 3: # Turn left
            m1 = Velocity(turn_speed)
            m2 = Velocity(speed)
        elif direction == 4: # Turn right
            m1 = Velocity(speed)
            m2 = Velocity(turn_speed)
        else:
            print(stop())
            print("Invalid direction selected! Options are 1 to 4.")
            return
        
        # Send the speed to motors
        send_speeds(m1,m2)
        
    except ValueError:
        print(stop())
        print("Invalid number entered, enter a integer.")
        return
    
    return
