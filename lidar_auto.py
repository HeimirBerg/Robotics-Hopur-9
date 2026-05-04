from lidarprufa import start_lidar, stop_lidar, sense, _min_dist_in_zone, _latest_scan, _scan_lock, FRONT_ZONE, LEFT_ZONE, RIGHT_ZONE
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

                with _scan_lock:
                    scan = list(_latest_scan)
                front = _min_dist_in_zone(scan, *FRONT_ZONE)
                left  = _min_dist_in_zone(scan, *LEFT_ZONE)
                right = _min_dist_in_zone(scan, *RIGHT_ZONE)
                print(f"front={front:.0f}cm  left={left:.0f}cm  right={right:.0f}cm  s0={s0:.0f}  s1={s1:.0f}  merki={merki}")

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
        stop_lidar()