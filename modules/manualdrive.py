"""
--- Handvirk keyrsla / Manual Driving Module ---

Finnur lyklaborð og fjastýringar tengdar við Pi.
Gefur notenda valmöguleika á milli tækja og
velur sjálfvirkt hvaða keyrslu fall á að nota.
"""

import evdev # type: ignore
import time

from config import Speed, TurnStage
import hreyfing as m
# TODO: import movement as m


def find_input_devices() -> None:
    """Finnur öll tæki í möppunni `/dev/input/` og prentar þau í Terminal."""

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    if not devices:
        print("\nFann engin tæki!\n")
    else:
        # Prenta töflu
        print("\nFann tækin:")
        for device in devices:
            print(device.path, device.name, device.phys, sep=" || ")
        print("====== BÚINN ======\n")


def select_input_device(device_name: str) -> str | None:
    """
    Leitar að möppu slóðinni fyrir valið tæki (lyklaborði/fjarstýringu).

    :input_name: Hluti af nafni tækis, t.d. Dell eða Keyboard (Nöfn sjást með fallinu `find_input_devices`).
    :return: Slóð á völdu inntakstæki. Ef tækið finnst ekki er skilað `None`.
    """

    try:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if device_name.lower() in device.name.lower():
                return device.path
        
        # Prentar aðeins ef for-lykkja klárast án þess að skila slóð
        print("Fann ekki tækið sem þú leitaðir að.\n")
        return None
    
    except ValueError:
        print("Ógilt nafn slegið inn. Þarf að vera strengur.\n")
        return None


def calculate_speeds(reference_time: float, init_speed: Speed, init_turn: TurnStage) -> tuple[Speed, TurnStage]:
    """
    Reiknar aukinn hraða og beygju hraða eftir ákveðna seinkun.
    
    :reference_time: Viðmiðunar tími í reikningum.
    :init_speed: Upphafs hraði.
    :init_turn: Upphafs beygju stig.
    :return: Útreiknaður hraði og beygju skref í túplu.
    """

    MIN_SPEED = Speed(15)   # Minnsti hraði sem er hægt að senda á mótora
    MAX_SPEED = Speed(255)  # Mesti hraði sem er hægt að senda á mótora
    MIN_TURN = TurnStage(-1)    # Minnsta beygja sem er hægt að taka
    MAX_TURN = TurnStage(3)     # Mesta beygja sem er hægt að taka
    SPEED_BOOST = Speed(50) # Hraði sem er bætt við þegar takka hefur verið haldi í biðtíma
    WAIT_TIME_1: int = 3  # [s]
    WAIT_TIME_2: int = 10 # [s]

    # Hjálpar fall til að losna við if setningar
    def clamp(low, value, high):
        """Klemmir gildi á milli `low` (MIN) og `high` (MAX)."""
        return max(low, min(value, high))

    # Tími liðinn frá því fyrsta takka var ýtt niður.
    elapsed_time: float = time.time() - reference_time

    if elapsed_time >= WAIT_TIME_2:
        speed = clamp(MIN_SPEED, (init_speed + (SPEED_BOOST * 2)), MAX_SPEED)
        turn = clamp(MIN_TURN, (init_turn + 2), MAX_TURN)

    elif elapsed_time >= WAIT_TIME_1:
        speed = clamp(MIN_SPEED, (init_speed + SPEED_BOOST), MAX_SPEED)
        turn = clamp(MIN_TURN, (init_turn + 1), MAX_TURN)

    else:
        speed = init_speed
        turn = init_turn

    return speed, turn


def get_new_speed() -> Speed:
    """Spyr notanda um nýjann hraða."""

    speed: Speed | None = None  # Valinn hraði
    
    while speed is None:
        try:
            speed = Speed(input("Veldu nýjann hraða á bilinu [15 til 255]: "))
    
        except ValueError as _e:
            speed = None
            print(f"Ógildur hraði sleginn inn. {_e}.")
    
    return speed


def get_new_turn() -> TurnStage:
    """Spyr notanda um nýtt beygju skref."""

    turn: TurnStage | None = None  # Sjálfgefið beygju skref

    while turn is None:
        try:
            turn = TurnStage(input("Veldu nýtt beygju skref á bilinu [-1 til 3]: "))
        
        except ValueError as _e:
            turn = None
            print(f"Ógilt beygju skref valið. {_e}.")

    return turn


def keyboard_control(device_path: str) -> None:
    """Stýri- og keyrsluvirkni með lyklaborði."""
    
    device = evdev.InputDevice(device_path) # Slóðin á lyklaborðið

    keys_held: set[str] = set() # Mengi með tökkum sem er haldið inni
    init_speed = Speed(100)       # Upphafs/sjálfgefinn hraði [15 til 255]
    init_turn_stage = TurnStage(0)    # Upphafs/sjálfgefinn beygju stig [-1 til 3]
    start_time: float = 0.0     # Tími tekinn þegar fyrsta takka er ýtt niður [s]

    print("=== Tilbúinn í keyrslu með lyklaborði ===")

    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                key = evdev.categorize(event)

                # Þegar takka er ýtt niður
                if key.keystate in (key.key_down, key.key_hold):

                    # Tek tímann þegar fyrsta takka er ýtt niður
                    if (key.keystate == key.key_down) and not keys_held:
                        start_time = time.time()
                    
                    # Bæti takkanum í mengið
                    keys_held.add(key.keycode)

                    # Reikna hraðana eftir seinkun
                    speed, turn_stage = calculate_speeds(start_time, init_speed, init_turn_stage)

                    # Framkvæmi virkni eftir hvaða takka er ýtt niður, hef beygjur efst svo þær taki forgang.
                    if key.keycode in ("KEY_LEFT", "KEY_A"):
                        m.drive(speed, 3, turn_stage)

                    elif key.keycode in ("KEY_RIGHT", "KEY_D"):
                        m.drive(speed, 4, turn_stage)
                    
                    elif key.keycode in ("KEY_UP", "KEY_W"):
                        m.drive(speed, 1)

                    elif key.keycode in ("KEY_DOWN", "KEY_S"):
                        m.drive(speed, 2)

                    elif key.keycode == "KEY_F":
                        m.stop()
                        init_speed = get_new_speed()

                    elif key.keycode == "KEY_R":
                        m.stop()
                        init_turn_stage = get_new_turn()

                    elif key.keycode == "KEY_SPACE":
                        m.stop()
                        print(f"=== Hætti í keyrslu ===\n{"Bless, bless...":^23}")
                        return

                # Þegar takka er sleppt
                elif key.keystate == key.key_up:
                    keys_held.discard(key.keycode) # Tek takkann úr mengi
                    if not keys_held:
                        start_time = 0.0
                        m.stop()  # Stoppar bara þegar búið er að sleppa öllum tökkum

    # Önnur leið til að hætta í keyrslu og forriti
    except KeyboardInterrupt:
        m.stop()
        print(f"=== Hætti í keyrslu ===\n{"Úps...":^23}")
        return

# TODO: Á eftir að útfæra
def ps5_control(device_path: str) -> None:
    """Stýri- og keyrsluvirkni með PlayStation fjarstýringu."""
    raise NotImplementedError


def manual() -> None:
    """Keyrir handvirka keyrslu, föll og virkni."""

    input_name: str = ""
    input_path: str | None = None 
    
    # Prenta tiltæk tæki.
    find_input_devices()

    while input_path is None:
        input_name = input("Sláðu inn nafn lyklaborðs eða fjarstýringar: ")
        input_path = select_input_device(input_name)

    if "ps" in input_name.lower():  # ? Á kannski eftir að breytast
        ps5_control(input_path)
    else:
        keyboard_control(input_path)


# Test code
if __name__ == "__main__":
    manual()
