from sensor import *
from movement import *
import time

# ------Fastar------
speed      = 200
start_turn = 120
sd         = 50  

# ------ Svæði ------
zone_a_wide   = set(range(315, 360)) | set(range(0, 46))  # Fram — vítt — snemma uppgötvun
zone_a_narrow = set(range(345, 360)) | set(range(0, 16))  # Fram — þröngt — beint framundan
zone_b = set(range(45, 136))                               # Hægri
zone_c = set(range(135, 226))                              # Aftur
zone_d = set(range(225, 316))                              # Vinstri
degTime = 1.0 / 64.8                                      # Tíma fasti til að snúa bílnum

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

            FrontClose = under(snapshot, zone_a_wide, start_turn)   # Vítt — byrjar að beygja snemma
            FrontStop  = under(snapshot, zone_a_narrow, sd)         # Þröngt — stoppar bara ef beint framundan
            RightClose = under(snapshot, zone_b, sd)
            LeftClose  = under(snapshot, zone_d, sd)

            right_clear = min_distance(snapshot, zone_b)
            left_clear  = min_distance(snapshot, zone_d)
            front_dist  = min_distance(snapshot, zone_a_wide)       # nálægasta hindrun framundan

            print(f"front: {front_dist:.0f}cm  FrontClose: {FrontClose}  FrontStop: {FrontStop}  L: {LeftClose}  R: {RightClose}")

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
                    auto_calculate_turn("Vinstri", front_dist, speed)
                else:
                    auto_calculate_turn("Hægri", front_dist, speed)

            elif FrontStop:
                if not LeftClose and not RightClose:
                    if left_clear > right_clear:
                        drive(speed, 3, -1)  # snúa á staðnum til vinstri
                    else:
                        drive(speed, 4, -1)  # snúa á staðnum til hægri

                elif LeftClose and not RightClose:
                    drive(speed, 4, -1)      # snúa á staðnum til hægri

                elif RightClose and not LeftClose:
                    drive(speed, 3, -1)      # snúa á staðnum til vinstri

                else:
                    stop()
                    time.sleep(0.5)
                    if left_clear + right_clear < 33:
                        send_speeds(-speed, -speed)
                        time.sleep(0.5)
                        stop()
                        time.sleep(0.5)
                    snapshot = get_snapshot()
                    heading, direction = findExit(snapshot)
                    print(f"FrontStop — best exit: {heading}° → {direction}")
                    turnToExit(heading, direction)

            time.sleep(0.1)

    finally:
        stop_lidar()  # Stoppar LiDAR þegar autopilot hættir