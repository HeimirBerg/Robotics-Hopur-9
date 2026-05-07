from lidarprufa import *
from hreyfing import *

import time

# --- Fastar ---
speed     = 100
min_distance = 30   # Hvenær á að byrja að bakka
max_distance = 80   # Hvenær hann á að byrja að beygja

def autopilot():
    start_lidar()
    print("Autopilot running.")

    try:
        while True:
            front = get_distance(315, 45)
            left  = get_distance(225, 315)
            right = get_distance(45, 135)

            print(f"front: {front:.0f}  left: {left:.0f}  right: {right:.0f}")

            if front > max_distance:
                fara_afram(speed)

            elif left > right:
                # turn left — sharper if front is very close
                inner = int(speed * front / max_distance)
                beygja("Vinstri", speed, inner)

            elif right >= left:
                # turn right — sharper if front is very close
                inner = int(speed * front / max_distance)
                beygja("Hægri", speed, inner)

            else:
                fara_aftur(speed)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()