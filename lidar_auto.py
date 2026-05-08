from lidarprufa import start_lidar, stop_lidar, get_distance
from hreyfing import *

import time
from collections import deque

# --- Fastar ---
speed         = 150
turn_distance = 80   # cm — start turning
stop_distance = 20   # cm — stop and spin in place
STUCK_THRESHOLD = 3  # cm — how little movement counts as stuck
STUCK_TIME      = 15 # how many readings before declaring stuck

recent_fronts = deque(maxlen=STUCK_TIME)


def is_stuck():
    if len(recent_fronts) < STUCK_TIME:
        return False
    if min(recent_fronts) > turn_distance:  # all readings clear — not stuck
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

                # Back up only if there's room behind
                rear = get_distance(135, 225)
                if rear > 40:
                    print(f"Backing up (rear clear: {rear:.0f}cm)...")
                    fara_aftur(speed)
                    time.sleep(0.5)
                else:
                    print(f"Rear too close ({rear:.0f}cm), skipping backup.")

                # Spin in place — both wheels opposite directions
                turn_dir = "Vinstri" if left > right else "Hægri"
                print(f"Spinning {turn_dir}...")
                while get_distance(300, 60) <= turn_distance:
                    beygja(turn_dir, speed, -speed)
                    time.sleep(0.1)
                print("Stuck resolved.")

            elif front > turn_distance:
                fara_afram(speed)

            elif front > stop_distance:
                # ratio: 1.0 when far away, 0.0 when at stop_distance
                ratio = (front - stop_distance) / (turn_distance - stop_distance)

                # Outer wheel slows down as obstacle gets closer
                outer = int(speed * (0.5 + 0.5 * ratio))  # range: half speed → full speed

                # Inner wheel slows much more — tighter curve when close
                inner = int(speed * ratio * ratio)         # range: 0 → full speed

                if left > right:
                    beygja("Vinstri", outer, inner)
                else:
                    beygja("Hægri", outer, inner)

            else:
                turn_dir = "Vinstri" if left > right else "Hægri"
                print(f"Too close! Spinning {turn_dir}...")
                while get_distance(300, 60) <= stop_distance:
                    beygja(turn_dir, speed, 0)
                    time.sleep(0.1)

            time.sleep(0.1)

    finally:
        stop_lidar()