from sensor import *
from movement import *
import time

# ------Fastar------
speed      = 150
start_turn = 60
sd         = 20  

# ------ Svæði ------
zone_a = set(range(315, 360)) | set(range(0, 46))  # Fram
zone_b = set(range(45, 136))                        # Hægri
zone_c = set(range(135, 226))                       # Aftur
zone_d = set(range(225, 316))                       # Vinstri
degTime = 1.0 / 167.9                               # Tíma fasti til að snúa bílnum ATH þarf örgl að uppfæra með nýja boddí

def findExit(snapshot):
    full = [snapshot.get(a, MaxRange) for a in range(360)]
    smoothed = [
        sum(full[(a + i) % 360] for i in range(-15, 16)) / 31
        for a in range(360)
    ]
    best_angle = max(range(360), key=lambda a: smoothed[a])
    direction  = "Hægri" if 1 <= best_angle <= 179 else "Vinstri"
    print(f"Best exit: {best_angle}° → {direction}")
    return best_angle, direction

def turnToExit(heading, direction):
    if direction == "Hægri":
        angle   = heading
        dir_num = 4
    else:
        angle   = 360 - heading
        dir_num = 3
    if angle < 2:
        return
    duration = angle * degTime
    print(f"Spinning {direction} {angle}° → {duration:.3f}s")
    drive(255, dir_num, -1)
    time.sleep(duration)
    stop()
    time.sleep(0.4)

def autopilot():
    start_lidar()  # Byrjar LiDAR í bakgrunni
    print("Autopilot running.")
    try:
        while True:
            snapshot = get_snapshot()

            FrontClose = under(snapshot, zone_a, start_turn)
            FrontStop  = under(snapshot, zone_a, sd)
            RightClose = under(snapshot, zone_b, sd)
            LeftClose  = under(snapshot, zone_d, sd)

            right_clear = zone_clearance(snapshot, zone_b)
            left_clear  = zone_clearance(snapshot, zone_d)
            front_dist  = min_distance(snapshot, zone_a)  # nálægasta hindrun framundan

            if not FrontStop and not FrontClose:
                # ------ keyra áfram ------
                if LeftClose and not RightClose:
                    auto_calculate_turn("Hægri", front_dist, speed)   # Smávegis til hægri á meðan við keyrum áfram
                elif RightClose and not LeftClose:
                    auto_calculate_turn("Vinstri", front_dist, speed)  # Smávegis til vinstri á meðan við keyrum áfram
                else:
                    send_speeds(speed, speed)  # Keyra beint áfram

            elif FrontClose and not FrontStop:
                # ------ Eitthvað framundan en enn pláss — rólegt beygja ------
                if left_clear > right_clear:
                    auto_calculate_turn("Vinstri", front_dist, speed)  # Beygja smá til vinstri
                else:
                    auto_calculate_turn("Hægri", front_dist, speed)    # Beygja smá til hægri

            elif FrontStop:
                # ------ Of nálægt framundan — stoppa og finna besta útveg ------
                stop()
                time.sleep(0.2)

                if LeftClose and RightClose and (left_clear + right_clear) < 33:
                    # Of þröngt — bakka fyrst
                    send_speeds(-speed, -speed)
                    time.sleep(0.5)
                    stop()
                    time.sleep(0.2)

                # Skanna og snúa í bestu átt
                snapshot = get_snapshot()
                heading, direction = findExit(snapshot)
                turnToExit(heading, direction)

            time.sleep(0.1)

    finally:
        stop_lidar()  # Stoppar LiDAR þegar autopilot hættir