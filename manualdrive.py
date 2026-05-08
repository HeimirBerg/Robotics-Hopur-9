"""
--- Handvirk keyrsla / Manual Driving Module ---

Finnur lyklaborð og fjastýringar tengdar við Pi.
Gefur notenda valmöguleika á milli tækja og
velur sjálfvirkt hvaða keyrslu fall á að nota.
"""

import evdev # type: ignore
import time

import movement as m


SPEED_BOOST: int = 50  # Hraði sem er bætt við þegar takka hefur verið haldi í biðtíma
WAIT_TIMES: tuple[int, int] =  (3, 10)  # [s]


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


def select_input_device() -> tuple[str, str]:
    """
    Leitar að möppu slóðinni fyrir valið tæki (lyklaborði/fjarstýringu).

    :return: Nafn og slóð á valið tæki.
    """

    name: str | None = None
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    while name is None:
        try:
            name = input("Sláðu inn nafn eða slóð lyklaborðs eða fjarstýringar: ")

            for device in devices:
                if name.lower() in device.name.lower():
                    return device.name, device.path
                elif name.lower() in device.path.lower(): 
                    return device.name, device.path
            
            # Prentar aðeins ef for-lykkja klárast án þess að skila slóð
            name = None
            print("Fann ekki tækið sem þú leitaðir að.\n")
        
        except ValueError:
            name = None
            print("Ógilt nafn slegið inn. Þarf að vera strengur.\n")


def keyboard_control(device_path: str) -> None:
    """Stýri- og keyrsluvirkni með lyklaborði."""
    
    device = evdev.InputDevice(device_path) # Slóðin á lyklaborðið

    keys_held: set[str] = set() # Mengi með tökkum sem er haldið inni
    init_speed: int = 100       # Upphafs/sjálfgefinn hraði [15 til 255]
    init_turn_stage: int = 0    # Upphafs/sjálfgefinn beygju stig [-1 til 3]
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
                    speed, turn_stage = m.calculate_boosts(start_time, init_speed, init_turn_stage, SPEED_BOOST, WAIT_TIMES)

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
                        init_speed = m.get_new_speed()

                    elif key.keycode == "KEY_R":
                        m.stop()
                        init_turn_stage = m.get_new_turn_stage()

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
        print(f"=== Hætti í keyrslu ===")
        return


# TODO: Á eftir að útfæra
def ps5_control(device_path: str) -> None:
    """Stýri- og keyrsluvirkni með PlayStation fjarstýringu."""
    raise NotImplementedError

    # Held að þetta verði bara eins og keyboard control nema með öðrum tökkum.


def manual() -> None:
    """Keyrir handvirka keyrslu, föll og virkni."""
    
    # Prenta tiltæk tæki.
    find_input_devices()

    # Vel inntak
    input_name, input_path = select_input_device()

    if "controller" in input_name.lower():  # ? Á kannski eftir að breytast
        ps5_control(input_path)
    else:
        keyboard_control(input_path)


# Test code
if __name__ == "__main__":
    manual()
