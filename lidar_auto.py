from lidarprufa import start_lidar, stop_lidar, get_distance
from hreyfing import *

import time

# --- Settings ---
HRADI     = 100
TOO_CLOSE = 30   # cm — back up if everything is this close
TURNING   = 80   # cm — start turning if front is closer than this


def get_action():
    """Read LiDAR sectors and decide what to do."""
    front = get_distance(315, 45)   # wider front — 90° arc
    left  = get_distance(225, 315)  # left side
    right = get_distance(45, 135)   # right side

    if front > TURNING and left > TOO_CLOSE and right > TOO_CLOSE:
        return "forward", 0

    elif left > right:
        return "left", left   # pass room so beygja can scale the turn

    elif right >= left:
        return "right", right

    else:
        return "back", 0


def autopilot():
    start_lidar()
    print("Autopilot running.")

    try:
        while True:
            action, room = get_action()

            if action == "forward":
                fara_afram(HRADI)

            elif action == "left":
                radius = int(HRADI * min(room, 100) / 100)
                beygja("Vinstri", HRADI, radius)

            elif action == "right":
                radius = int(HRADI * min(room, 100) / 100)
                beygja("Hægri", HRADI, radius)

            elif action == "back":
                fara_aftur(HRADI)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()