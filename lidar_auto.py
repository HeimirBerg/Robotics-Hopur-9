from lidarprufa import sense, start_lidar, stop_lidar
from hreyfing import *

import time

# Distance thresholds (cm)
CLEAR     = 80   # far enough to go straight
TURNING   = 30   # close enough to start turning
TOO_CLOSE = 15   # last resort — back up

HRADI = 200


def autopilot():
    start_lidar()
    print("LiDAR ready — autopilot running.")

    try:
        while True:
            front, front_left, front_right = sense()

            if front > CLEAR and front_left > CLEAR and front_right > CLEAR:
                # All clear ahead — go straight
                fara_afram(HRADI)

            elif front_left > front_right:
                # More room on the left — turn left
                radius = int(HRADI * (front_left / 100))
                radius = max(0, min(radius, HRADI))
                beygja("Vinstri", HRADI, radius)

            elif front_right >= front_left:
                # More room on the right — turn right
                radius = int(HRADI * (front_right / 100))
                radius = max(0, min(radius, HRADI))
                beygja("Hægri", HRADI, radius)

            if front < TOO_CLOSE and front_left < TOO_CLOSE and front_right < TOO_CLOSE:
                # Completely boxed in — back up as last resort
                fara_aftur(HRADI)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()