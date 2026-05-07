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
                reikna_beygju("Vinstri", left, speed)

            elif right >= left:
                reikna_beygju("Hægri", right, speed)
            else:
                fara_aftur(speed)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()