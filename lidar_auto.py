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
                print(f"s0={s0:.0f} s1={s1:.0f} → TURN HARD RIGHT (danger)")
                beygja("Hægri", hradi, -hradi)

            elif s0 > 100 and s1 > 100:
                print(f"s0={s0:.0f} s1={s1:.0f} → FORWARD")
                fara_afram(hradi)

            elif s0 > 100 and s1 <= 100:
                radius = int(hradi * (s1 - 20) / 80)
                print(f"s0={s0:.0f} s1={s1:.0f} → TURN LEFT")
                beygja("Vinstri", hradi, max(0, radius))

            elif s1 > 100 and s0 <= 100:
                radius = int(hradi * (s0 - 20) / 80)
                print(f"s0={s0:.0f} s1={s1:.0f} → TURN RIGHT")
                beygja("Hægri", hradi, max(0, radius))

            else:
                print(f"s0={s0:.0f} s1={s1:.0f} → TURN HARD RIGHT (blocked)")
                beygja("Hægri", hradi, -hradi)

            time.sleep(0.05)

    finally:
        stop_lidar()