from lidarprufa import start_lidar, stop_lidar, get_distance
from hreyfing import *

import time

# --- Thresholds (cm) ---
TOO_CLOSE = 30   # back up if everything is this close
TURNING   = 80   # start turning if front is closer than this

HRADI = 200


def autopilot():
    start_lidar()
    print("Autopilot running.")

    try:
        while True:
            front = get_distance(345, 15)
            left  = get_distance(315, 345)
            right = get_distance(15,  45)

            if front > TURNING and left > TOO_CLOSE and right > TOO_CLOSE:
                # all clear — go straight
                fara_afram(HRADI)

            elif left > right:
                # more room on the left — turn left
                beygja("Vinstri", HRADI, -HRADI)

            elif right >= left:
                # more room on the right — turn right
                beygja("Hægri", HRADI, -HRADI)

            else:
                # truly stuck — back up as last resort
                fara_aftur(HRADI)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()