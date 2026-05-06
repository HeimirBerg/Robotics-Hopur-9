from lidarprufa import sense, start_lidar, stop_lidar
from hreyfing import *
import time


def autopilot():
    hradi = 200
    TOO_CLOSE = 30   # cm

    start_lidar()
    print("LiDAR ready — autopilot running.")

    try:
        while True:
            try:
                s0, s1, _ = sense()
            except Exception:
                time.sleep(0.1)
                continue

            if s0 > TOO_CLOSE and s1 > TOO_CLOSE:
                fara_afram(hradi)

            elif s0 > TOO_CLOSE and s1 <= TOO_CLOSE:
                # right blocked, turn left
                beygja("Vinstri", hradi, -hradi)

            elif s1 > TOO_CLOSE and s0 <= TOO_CLOSE:
                # left blocked, turn right
                beygja("Hægri", hradi, -hradi)

            else:
                # both blocked, back up
                fara_aftur(hradi)
                time.sleep(0.5)

            time.sleep(0.1)

    finally:
        stop_lidar()