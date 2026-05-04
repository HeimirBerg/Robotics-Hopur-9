# ---------- Fjastýringar --------- #
# Finnur input frá keyboard eða PS5 controller

import evdev

# def get_device_path(device_number: int = 0) -> str:
#     path = f"/dev/input/event{device_number}"
#     return path

def find_input_devices() -> None:
    """
    Fall sem finnur öll innput tæki í möpunni \"/dev/input/\".

    :Return: Prentar í Terminal lista með [path, name, phys].
    """
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    print("\nFound devices:")
    for device in devices:
        print(device.path, device.name, device.phys, sep="|")
    print("--- END ---\n")

def select_input_device(device_name: str) -> None:
    """
    Velur input tæki í möppunni \"/dev/input/\" eftir nafni tækisins.

    :device_name: Nafn tækisins. Miðju gildið í lista með tækjum \"path -- name -- phys\".
    :Skilar: Slóðinni á tækið með device.path.
    """

    pass

# if __name__ == "__main__":
#     path = get_device_path(2)
#     print(path)
#     keyboard = InputDevice(path)

#     for event in keyboard.read_loop():
#         if event.type == ecodes.EV_KEY:
#             key = categorize(event)
            
#             if key.keystate == key.key_down or key.keystate == key.key_hold:
#                 if key.keycode == 'KEY_W':
#                     print("Er hér í w")
#                 elif key.keycode == 'KEY_S':
#                     print("Er hér í s")
#                 elif key.keycode == 'KEY_A':
#                     print("Er hér í a")
#                 elif key.keycode == 'KEY_D':
#                     print("Er hér í d")
                    
#             elif key.keystate == key.key_up:
#                 print("Fór hingað")

# Test code
if __name__ == "__main__":
    find_input_devices()
    select_input_device()
