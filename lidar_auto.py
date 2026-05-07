from lidarprufa import *
from hreyfing import *

import time

# --- Fastar ---
speed         = 150
turn_distance = 120  # cm — start turning
stop_distance = 20    # Hvenær hann á að byrja að beygja

def autopilot():
    start_lidar()
    print("Autopilot running.")

    try:
        while True:
            front = get_distance(315, 45)
            left  = get_distance(225, 315)
            right = get_distance(45, 135)

            print(f"front: {front:.0f}  left: {left:.0f}  right: {right:.0f}")

            if front > turn_distance:
                # all clear — go straight
                fara_afram(speed)

            elif front > stop_distance:
                # getting close — gentle arc away
                inner = int(speed * front / turn_distance)
                if left > right:
                    beygja("Vinstri", speed, inner)
                else:
                    beygja("Hægri", speed, inner)

            else:
                # too close — stop and spin in place
                stoppa()
                time.sleep(0.2)
                if left > right:
                    beygja("Vinstri", speed, -speed)
                else:
                    beygja("Hægri", speed, -speed)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()