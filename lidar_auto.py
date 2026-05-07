from lidarprufa import *
from hreyfing import *

import time

HRADI = 200


def autopilot():
    start_lidar()
    print("Autopilot running.")

    try:
        while True:
            action = get_action()

            if action == "forward":
                fara_afram(HRADI)

            elif action == "left":
                beygja("Vinstri", HRADI, -HRADI)

            elif action == "right":
                beygja("Hægri", HRADI, -HRADI)

            elif action == "back":
                fara_aftur(HRADI)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()