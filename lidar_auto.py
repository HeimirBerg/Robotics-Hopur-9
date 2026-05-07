from lidarprufa import *
from hreyfing import *

import time

# --- Fastar ---
speed     = 70
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
            if front > max_distance and left > min_distance and right > min_distance:
                fara_afram(speed)
                print(front)

            elif left > right:
                reikna_beygju("Vinstri", left, speed)
                print(left)
            elif right >= left:
                reikna_beygju("Hægri", right, speed)
                print(right)
            else:
                fara_aftur(speed)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()