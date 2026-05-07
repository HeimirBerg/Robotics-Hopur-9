from lidarprufa import start_lidar, stop_lidar, get_distance
from hreyfing import *

import time
from collections import deque

# --- Fastar ---
speed         = 255
turn_distance = 80   # cm — start turning
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
            front = get_distance(300, 60)
            right = get_distance(45, 135)
            left  = get_distance(225, 315)

            recent_fronts.append(front)

            print(f"front: {front:.0f}  left: {left:.0f}  right: {right:.0f}")

            if is_stuck():
                print("Stuck! Turning around...")
                recent_fronts.clear()
                fara_aftur(speed)
                time.sleep(0.8)
                turn_dir = "Vinstri" if left > right else "Hægri"
                # Keep turning until front is clear
                while get_distance(300, 60) <= turn_distance:
                    beygja(turn_dir, speed, 0)
                    time.sleep(0.1)
                print("Stuck resolved.")

            elif front > turn_distance:
                fara_afram(speed)

            elif front > stop_distance:
                inner = int(speed * front / turn_distance)
                if left > right:
                    beygja("Vinstri", speed, inner)
                else:
                    beygja("Hægri", speed, inner)

            else:
                turn_dir = "Vinstri" if left > right else "Hægri"
                print(f"Too close! Spinning {turn_dir}...")
                # Keep spinning until front is clear
                while get_distance(300, 60) <= stop_distance:
                    beygja(turn_dir, speed, 0)
                    time.sleep(0.1)

            time.sleep(0.1)

    finally:
        stop_lidar()