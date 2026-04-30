# ---------- Main ---------- #
# Þetta er kóðinn sem Lalli mun keyra.
# Hér er kallað á föll úr modules og kóði til að kveikja og slökkva á Raspberry Lalli.

import src.motorcontrol as mc

# Setup
req_speed = -1

# Select speed
while not (15 <= req_speed <= 255):
    try:
        req_speed = int(input("Select speed: "))

        # Check if speed in range
        if not (15 <= req_speed <= 255):
            print("Select speed in ragne [15-255].")
            continue
        else:
            break

    except ValueError:
        print("Invalid number format.")
        continue

# Select options
while True:
    print("Select options:\n w) Forward\n s) Reverse\n a) Turn left\n d) Turn right\n q) Stop\n e) Set speed")
    
    try:
        selection = input("Selection: ")

        if selection == "w":
            print(mc.forward(req_speed))

        elif selection == "s":
            print(mc.reverse(req_speed))

        elif selection == "a":
            print(mc.turn_left(req_speed))

        elif selection == "d":
            print(mc.turn_right(req_speed))

        elif selection == "q":
            print(mc.stop())

        elif selection == "e":
            req_speed = int(input("Select speed: "))

        else:
            print("Invalid selection.")
            continue
        
    except KeyboardInterrupt:
        mc.stop()
        print("\n\nExiting...")
        break
    except ValueError:
        print("Invalid format.")
        continue

