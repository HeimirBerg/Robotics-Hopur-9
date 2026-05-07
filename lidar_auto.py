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

            if front > max_distance and left > min_distance and right > min_distance:
                fara_afram(speed)

            elif left > right:
                radius = int(speed * min(left, 100) / 100)
                beygja("Vinstri", speed, radius)

            elif right >= left:
                radius = int(speed * min(right, 100) / 100)
                beygja("Hægri", speed, radius)

            else:
                fara_aftur(speed)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()