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
                # Too close — back up to create space, then turn away
                fara_aftur(hradi)
                time.sleep(0.5)
                # Turn toward whichever side has more room
                if s0 >= s1:
                    beygja("Vinstri", hradi, -hradi)
                else:
                    beygja("Hægri", hradi, -hradi)
                time.sleep(0.4)

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
                # Both sides blocked — back up and turn right
                fara_aftur(hradi)
                time.sleep(0.5)
                beygja("Hægri", hradi, -hradi)
                time.sleep(0.4)

            time.sleep(0.1)

    finally:
        stop_lidar()