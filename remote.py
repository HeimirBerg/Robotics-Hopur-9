# ---------- Fjastýringar --------- #
# Finnur input frá keyboard eða PS5 controller

import evdev

import hreyfing as h

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


# Test code
if __name__ == "__main__":
    path = None

    find_input_devices()

    while path == None:
        name = input("Sláðu inn nafn lyklaborðs: ")
        path = select_input_device(name)

    print(path, "was selected.\n")

    speed = h.velja_hrada()
    radius = h.velja_radius(speed)

    keyboard = evdev.InputDevice(path)

    try:
        for event in keyboard.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                key = evdev.categorize(event)
                
                if key.keystate == key.key_down or key.keystate == key.key_hold:
                    if key.keycode == 'KEY_W':
                        h.fara_afram(speed)
                    elif key.keycode == 'KEY_S':
                        h.fara_aftur(speed)
                    elif key.keycode == 'KEY_A':
                        h.beygja("Vinstri", speed, radius)
                    elif key.keycode == 'KEY_D':
                        h.beygja("Hægri", speed, radius)
                    elif key.keycode == 'KEY_E':
                        speed = h.velja_hrada()
                    elif key.keycode == 'KEY_F':
                        radius = h.velja_radius(speed)
                        
                elif key.keystate == key.key_up:
                    h.stoppa()
                    print("Stoppaði!!!")
    except KeyboardInterrupt:
        h.stoppa()
        print("\n--- Ó fokk ---\n")
