from lidarprufa import sense, start_lidar, stop_lidar
from hreyfing import *

import time


def autopilot():
    s0, s1 = 200, 200
    hradi  = 200

    start_lidar()
    print("LiDAR ready — autopilot running.")

    try:
        while True:
            try:
                s0, s1, merki = sense(s0, s1)
            except Exception:
                time.sleep(0.1)
                continue

            if merki == 1:
                # Something dangerously close — turn hard right
                beygja("Hægri", hradi, -hradi)

            elif s0 > 100 and s1 > 100:
                # Both sides clear — go straight
                fara_afram(hradi)

            elif s0 > 100 and s1 <= 100:
                # Right side blocked — turn left
                radius = int(hradi * (s1 - 20) / 80)
                beygja("Vinstri", hradi, max(0, radius))

            elif s1 > 100 and s0 <= 100:
                # Left side blocked — turn right
                radius = int(hradi * (s0 - 20) / 80)
                beygja("Hægri", hradi, max(0, radius))

            else:
                # Both sides blocked — turn hard right
                beygja("Hægri", hradi, -hradi)

            time.sleep(0.1)

    finally:
        stop_lidar()