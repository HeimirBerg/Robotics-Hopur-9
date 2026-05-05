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

            if s0 > 100 and s1 > 100:
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

            elif s0 > 20:
                # Left has some room — sharp turn left
                beygja("Vinstri", hradi, -hradi)

            elif s1 > 20:
                # Right has some room — sharp turn right
                beygja("Hægri", hradi, -hradi)

            else:
                # Truly stuck — back up as last resort
                fara_aftur(hradi)
                time.sleep(0.5)
                beygja("Hægri", hradi, -hradi)
                time.sleep(0.4)

            time.sleep(0.1)

    finally:
        stop_lidar()