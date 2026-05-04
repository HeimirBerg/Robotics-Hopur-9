from lidarprufa import start_lidar, stop_lidar, sense
from hreyfing import *
import time

def autopilot():
    s0, s1 = 200, 200
    hradi = 50

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
                beygja("Hægri", hradi, -hradi)
                time.sleep(0.5)
            elif s0 > 100 and s1 > 100:
                fara_afram(hradi)
                time.sleep(0.05)
            elif s0 > 100 and s1 <= 100:
                radius = int(hradi * (s1 - 20) / 80)
                beygja("Vinstri", hradi, max(0, radius))
                time.sleep(0.3)
            elif s1 > 100 and s0 <= 100:
                radius = int(hradi * (s0 - 20) / 80)
                beygja("Hægri", hradi, max(0, radius))
                time.sleep(0.3)
            else:
                beygja("Hægri", hradi, -hradi)
                time.sleep(0.5)

    finally:
        stop_lidar