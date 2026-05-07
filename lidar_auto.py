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
            
            print(f"front: {front:.0f}  left: {left:.0f}  right: {right:.0f}")
            
            if front > max_distance:
                # front is clear — go forward
                fara_afram(speed)

            elif left > min_distance or right > min_distance:
                # front blocked but one side has room — turn that way
                if left > right:
                    reikna_beygju("Vinstri", left, speed)
                else:
                    reikna_beygju("Hægri", right, speed)

            else:
                # everything blocked — spin around and go back
                beygja("Hægri", speed, -speed)  # spin on the spot
                time.sleep(1.5)                  # enough to turn ~180°
                fara_aftur(speed)

            time.sleep(0.1)

    finally:
        stop_lidar()