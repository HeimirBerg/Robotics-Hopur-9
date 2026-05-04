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
        print(device.path, device.name, device.phys, sep=" || ")
    print("--- END ---\n")


def select_input_device(device_name: str) -> str | None:
    """
    Velur input tæki í möppunni \"/dev/input/\" eftir nafni tækisins.

    :device_name: Nafn tækisins. Miðju gildið í lista með tækjum \"path || name || phys\".
    :Skilar: Slóðinni á tækið með device.path. Ef tæki finnst ekki er skilað None
    """

    # Setup
    device_path = ""

    try:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if device_name.lower() == device.name.lower():
                device_path = device.path
                return device_path
            else:
                print("No device found.\n")
                return
            
    except ValueError:
        print("Invalid name entered. Enter a string.\n")
        return


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
    path = None

    find_input_devices()

    while path == None:
        name = input("Sláðu inn nafn lyklaborðs: ")
        path = select_input_device(name)

    print(path, "was selected.")
