# --- Taka tvö á manual, stýrt með lyklaborði eða PS controller --- #

import evdev
import time

import hreyfing as h


def find_input_devices() -> None:
    """
    Fall sem finnur öll input tæki í möpunni `/dev/input/`.

    :return: Prentar í Terminal lista með [path || name || phys].
    """

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    # Prenta töflu
    print("\nFound devices:")
    for device in devices:
        print(device.path, device.name, device.phys, sep=" || ")
    print("--- END ---\n")


def select_input_device(input_name: str) -> str | None:
    """
    Fall sem finnur slóðina á input tæki sem er óskað eftir.

    :input_name: Hluti af nafni tækis sem er valið (sést í prentuðum lista með `find_input_devices`).
    :return: Slóðin á input tæki sem óskað var eftir. Ef tækið finnst ekki er skilað `None`.
    """

    try:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if input_name.lower() in device.name.lower():
                return device.path
            else:
                print("No device found.\n")
                return
    
    except ValueError:
        print("Invalid name entered. Enter a string.\n")
        return
    

def keyboard_control(path: str) -> None:
    """
    Ætla ekki að reyna að útskýra hvað þetta gerir annað en að stjórna með lyklaborði wasd og arrow keys.
    """
    # Setup
    device = evdev.InputDevice(path)
    speed: int = 100
    turn_stage: int = 1

    try:
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                key = evdev.categorize(event)

                if (key.keystate == key.key_down) or (key.keystate == key.key_hold):
                    if (key.keycode == "KEY_W") or (key.keycode == "KEY_UP"):
                        h.drive(speed, 1)
                        time.sleep(3)
                        if (speed + 50) <= 255:
                            speed += 50
                        h.drive(speed, 1)
                        time.sleep(5)
                        if (speed + 50) <= 255:
                            speed += 50
                        h.drive(speed, 1)

                    elif (key.keycode == "KEY_S") or (key.keycode == "KEY_DOWN"):
                        h.drive(speed, 2)
                        time.sleep(3)
                        if (speed + 50) <= 255:
                            speed += 50
                        h.drive(speed, 2)
                        time.sleep(5)
                        if (speed + 50) <= 255:
                            speed += 50
                        h.drive(speed, 2)

                    elif (key.keycode == "KEY_A") or (key.keycode == "KEY_LEFT"):
                        h.drive(speed, 3, turn_stage)
                        time.sleep(5)
                        h.drive(speed, 3, turn_stage - 1)
                        time.sleep(10)
                        h.drive(speed, 3, turn_stage - 2)

                    elif (key.keycode == "KEY_D") or (key.keycode == "KEY_RIGHT"):
                        h.drive(speed, 4, turn_stage)
                        time.sleep(5)
                        h.drive(speed, 4, turn_stage - 1)
                        time.sleep(10)
                        h.drive(speed, 4, turn_stage - 2)

                    elif (key.keycode == "KEY_SPACE") and (key.keystate == key.key_hold):
                        h.stop()
                        print("Hætti í keyrslu...Bless.")
                        return

                elif key.keystate == key.key_up:
                    h.stop()

    except KeyboardInterrupt:
        h.stop()
        print("\nMAY-DAY, MAY-DAY, MAY-DAY.\nAllt í rugli.\n")
        return


def ps5_control(path: str) -> None:
    ...


# Test code
if __name__ == "__main__":

    path = None

    find_input_devices()

    while path == None:
        name = input("Sláðu inn nafn lyklaborðs: ")
        path = select_input_device(name)

    print(path, "was selected.\n")

    keyboard_control(path)
