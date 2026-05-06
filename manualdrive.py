"""
Manual Driving module.

Selects input devices and assigns different control functions depending on selected input device.
"""

import evdev
import time

import hreyfing as h


def find_input_devices() -> None:
    """Finds all input devices under the folder `/dev/input/` and prints them to the Terminal."""

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    # Print table
    print("\nFound devices:")
    for device in devices:
        print(device.path, device.name, device.phys, sep=" || ")
    print("--- END ---\n")


def select_input_device(device_name: str) -> str | None:
    """
    Looks for the folder path for a requested input device.

    :input_name: Part of a input device's name, e.g. Dell or Keyboard. (Found with `find_input_devices` function).
    :return: The folder path to the requesten input device. If no divice is found returns `None`.
    """

    try:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if device_name.lower() in device.name.lower():
                return device.path
        
        # Prints only if for-loop finishes whithout returning
        print("No device found.\n")
        return None
    
    except ValueError:
        print("Invalid name entered. Enter a string.\n")
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

        h.drive(speed, direction, turn_stage)

        # Eftir annan biðtíma
        if (time.time() - start_time) >= wait_time_2:

            if direction in STRAIGHT and ((speed + SPEED_BOOZT) <= MAX_SPEED):
                speed += SPEED_BOOZT
            elif direction in TURN and (turn_stage != -1):
                turn_stage -= 1

            h.drive(speed, direction, turn_stage)

        elif event.keystate == event.key_up:
            h.stop()
            return
        
    elif event.keystate == event.key_up:
        h.stop()
        return
    

def keyboard_control(device_path: str) -> None:
    """Control logic using a keyboard."""
    
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
                        h.drive(speed, 1)
                        boozter(time_w, key, speed, 1)

                    elif (key.keycode == "KEY_S") or (key.keycode == "KEY_DOWN"):
                        if key.keystate == key.key_down:     
                            time_s = time.time()
                        h.drive(speed, 2)
                        boozter(time_s, key, speed, 2)

                    elif (key.keycode == "KEY_A") or (key.keycode == "KEY_LEFT"):
                        if key.keystate == key.key_down:
                            time_a = time.time()
                        h.drive(speed, 3, turn_stage)
                        boozter(time_a, key, speed, 3, turn_stage)

                    elif (key.keycode == "KEY_D") or (key.keycode == "KEY_RIGHT"):
                        if key.keystate == key.key_down: 
                            time_d = time.time()
                        h.drive(speed, 4, turn_stage)
                        boozter(time_d, key, speed, 4, turn_stage)

                    elif (key.keycode == "KEY_SPACE"):
                        h.stop()
                        print("Hætti í keyrslu...Bless.")
                        return

                elif key.keystate == key.key_up:
                    h.stop()

    except KeyboardInterrupt:
        h.stop()
        print("\nMAY-DAY, MAY-DAY, MAY-DAY.\nAllt í rugli.\n")
        return


def ps5_control(device_path: str) -> None:
    """Control logic using a PlayStation controller."""
    raise NotImplementedError


def manual() -> None:
    """Runs manual control functions"""

    input_name: str = ""
    input_path: str | None = None 
    find_input_devices()          # Print available devices

    while input_path is None:
        input_name = input("Sláðu inn nafn lyklaborðs eða fjarstýringu: ")
        input_path = select_input_device(input_name)

    if "ps" in input_name.lower():
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
