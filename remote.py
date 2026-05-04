# ---------- Fjastýringar --------- #
# Pickar upp input frá keyboard eða PS5 controller

import evdev
from evdev import InputDevice, categorize, ecodes

def get_device_path(device_number: int = 0) -> str:
    path = f"/dev/input/event{device_number}"
    return path




if __name__ == "__main__":
    path = get_device_path(2)
    print(path)
    keyboard = InputDevice(path)

    for event in keyboard.read_loop():
        if event.type == ecodes.EV_KEY:
            key = categorize(event)
            
            if key.keystate == key.key_down or key.keystate == key.key_hold:
                if key.keycode == 'KEY_W':
                    print("Er hér í w")
                elif key.keycode == 'KEY_S':
                    print("Er hér í s")
                elif key.keycode == 'KEY_A':
                    print("Er hér í a")
                elif key.keycode == 'KEY_D':
                    print("Er hér í d")
                    
            elif key.keystate == key.key_up:
                print("Fór hingað")