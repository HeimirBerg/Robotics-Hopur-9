from lidarprufa import start_lidar, stop_lidar, sense
from hreyfing import *
import time

def autopilot():
    s0, s1 = 200, 200
    hradi = 200

    start_lidar()

    try:
        while True:
            try:
                s0, s1, merki = sense(s0, s1)
            except Exception as e:
                print(f"Sense error: {e}")
                time.sleep(0.1)
                continue

            if merki == 1:
                # Too close — turn hard right for 0.5s then re-check
                beygja("Hægri", hradi, -hradi)
                time.sleep(0.5)

            elif s0 > 100 and s1 > 100:
                # Both clear — go forward
                fara_afram(hradi)
                time.sleep(0.05)

            elif s0 > 100 and s1 <= 100:
                # Obstacle on right — turn left
                radius = int(hradi * (s1 - 20) / 80)
                beygja("Vinstri", hradi, max(0, radius))
                time.sleep(0.3)

            elif s1 > 100 and s0 <= 100:
                # Obstacle on left — turn right
                radius = int(hradi * (s0 - 20) / 80)
                beygja("Hægri", hradi, max(0, radius))
                time.sleep(0.3)

            else:
                # Both blocked — turn hard right
                beygja("Hægri", hradi, -hradi)
                time.sleep(0.5)

    finally:
        stop_lidar()