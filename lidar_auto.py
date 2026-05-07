from lidarprufa import start_lidar, stop_lidar, get_distance
from hreyfing import *

import time
from collections import deque

# --- Fastar ---
speed         = 150
turn_distance = 180  # cm — start turning
stop_distance = 20   # cm — stop and spin in place
STUCK_THRESHOLD = 3  # cm — how little movement counts as stuck
STUCK_TIME      = 15 # how many readings before declaring stuck

recent_fronts = deque(maxlen=STUCK_TIME)


def is_stuck():
    if len(recent_fronts) < STUCK_TIME:
        return False
    return max(recent_fronts) - min(recent_fronts) < STUCK_THRESHOLD


def autopilot():
    start_lidar()
    print("Autopilot running.")

    try:
        while True:
            front = get_distance(315, 45)
            left  = get_distance(225, 315)
            right = get_distance(45, 135)

            recent_fronts.append(front)

            print(f"front: {front:.0f}  left: {left:.0f}  right: {right:.0f}")

            if is_stuck():
                print("Stuck! Turning around...")
                recent_fronts.clear()
                fara_aftur(speed)
                time.sleep(0.8)
                beygja("Hægri", speed, -speed)
                time.sleep(1.0)

            elif front > turn_distance:
                fara_afram(speed)

            elif front > stop_distance:
                inner = int(speed * front / turn_distance)
                if left > right:
                    beygja("Vinstri", speed, inner)
                else:
                    beygja("Hægri", speed, inner)

            else:
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