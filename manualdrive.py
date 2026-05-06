"""
--- Handvirk keyrsla / Manual Driving Module ---

Finnur lyklaborð og fjastýringar tengdar við Pi.
Gefur notenda valmöguleika á milli tækja og
velur sjálfvirkt hvaða keyrslu fall á að nota.
"""

import evdev
import time

import hreyfing as m
# import movement as m


def find_input_devices() -> None:
    """Finnur öll tæki í möppunni `/dev/input/` og prentar þau í Terminal."""

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    # Prenta töflu
    print("\nFann tækin:")
    for device in devices:
        print(device.path, device.name, device.phys, sep=" || ")
    print("====== BÚINN ======\n")


def select_input_device(device_name: str) -> str | None:
    """
    Leitar að möppu slóðinni fyrir völdu inntakstæki (lyklaborði/fjarstýringu).

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
    

def boozter(start_time: float, event, speed: int, direction: int, turn_stage: int = 0) -> None:
    """Merge with keybord control"""
    # Setup
    STRAIGHT: list[int] = [1, 2]
    TURN: list[int] = [3, 4]
    MAX_SPEED: int = 255
    SPEED_BOOZT: int = 50
    wait_time_1: int = 3
    wait_time_2: int = 8
    
    # Eftir fyrsta biðtíma
    if (time.time() - start_time) >= wait_time_1:

        if direction in STRAIGHT and ((speed + SPEED_BOOZT) <= MAX_SPEED):
            speed += SPEED_BOOZT
        elif direction in TURN and (turn_stage != -1):
            turn_stage -= 1

        m.drive(speed, direction, turn_stage)

        # Eftir annan biðtíma
        if (time.time() - start_time) >= wait_time_2:

            if direction in STRAIGHT and ((speed + SPEED_BOOZT) <= MAX_SPEED):
                speed += SPEED_BOOZT
            elif direction in TURN and (turn_stage != -1):
                turn_stage -= 1

            m.drive(speed, direction, turn_stage)

        elif event.keystate == event.key_up:
            m.stop()
            return
        
    elif event.keystate == event.key_up:
        m.stop()
        return
    

def keyboard_control(device_path: str) -> None:
    """Stýri- og keyrsluvirkni með lyklaborði."""
    
    device = evdev.InputDevice(device_path)
    speed: int = 100
    turn_stage: int = 1

    time_w: float = 0.0
    time_s: float = 0.0
    time_a: float = 0.0
    time_d: float = 0.0

    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                key = evdev.categorize(event)

                if (key.keystate == key.key_down) or (key.keystate == key.key_hold):
                    if (key.keycode == "KEY_W") or (key.keycode == "KEY_UP"):
                        if key.keystate == key.key_down:
                            time_w = time.time()
                        m.drive(speed, 1)
                        boozter(time_w, key, speed, 1)

                    elif (key.keycode == "KEY_S") or (key.keycode == "KEY_DOWN"):
                        if key.keystate == key.key_down:     
                            time_s = time.time()
                        m.drive(speed, 2)
                        boozter(time_s, key, speed, 2)

                    elif (key.keycode == "KEY_A") or (key.keycode == "KEY_LEFT"):
                        if key.keystate == key.key_down:
                            time_a = time.time()
                        m.drive(speed, 3, turn_stage)
                        boozter(time_a, key, speed, 3, turn_stage)

                    elif (key.keycode == "KEY_D") or (key.keycode == "KEY_RIGHT"):
                        if key.keystate == key.key_down: 
                            time_d = time.time()
                        m.drive(speed, 4, turn_stage)
                        boozter(time_d, key, speed, 4, turn_stage)

                    elif (key.keycode == "KEY_SPACE"):
                        m.stop()
                        print("Hætti í keyrslu...Bless.")
                        return

                elif key.keystate == key.key_up:
                    m.stop()

    except KeyboardInterrupt:
        m.stop()
        print("\nMAY-DAY, MAY-DAY, MAY-DAY.\nAllt í rugli.\n")
        return


def ps5_control(device_path: str) -> None:
    """Stýri- og keyrsluvirkni með PlayStation fjarstýringu."""
    raise NotImplementedError


def manual() -> None:
    """Keyrir handvirka keyrslu, föll og virkni."""

    input_name: str = ""
    input_path: str | None = None 
    find_input_devices()          # Prentar tiltæk tæki.

    while input_path is None:
        input_name = input("Sláðu inn nafn lyklaborðs eða fjarstýringar: ")
        input_path = select_input_device(input_name)

    if ("ps" or "cont") in input_name.lower():
        ps5_control(input_path)
    else:
        keyboard_control(input_path)


# Test code
if __name__ == "__main__":
    manual()

    # # Raw test code
    # path = None

    # find_input_devices()

    # while path is None:
    #     name = input("Sláðu inn nafn lyklaborðs: ")
    #     path = select_input_device(name)

    # print(path, "was selected.\n")

    # keyboard_control(path)
