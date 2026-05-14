from sensor import *
from movement import *
from collections import deque
import time

# ------Fastar------
speed      = 255
start_turn = 120
sd         = 50

STUCK_THRESHOLD = 3   # cm — hversu lítil hreyfing telst fastur
STUCK_TIME      = 15  # fjöldi lestrar áður en við segjum að hann sé fastur

# ------ Svæði ------
zone_a_wide   = set(range(315, 360)) | set(range(0, 46))  # Fram — vítt — snemma uppgötvun
zone_a_narrow = set(range(345, 360)) | set(range(0, 16))  # Fram — þröngt — beint framundan
zone_b = set(range(45, 136))                               # Hægri
zone_c = set(range(135, 226))                              # Aftur
zone_d = set(range(225, 316))                              # Vinstri
degTime = 1.0 / 64.8                                      # Tíma fasti til að snúa bílnum

recent_fronts = deque(maxlen=STUCK_TIME)

def is_stuck():
    if len(recent_fronts) < STUCK_TIME:
        return False
    if min(recent_fronts) > start_turn:  # allar lestur frjálsar — ekki fastur
        return False
    return max(recent_fronts) - min(recent_fronts) < STUCK_THRESHOLD

def escape_stuck(snapshot):
    recent_fronts.clear()
    print("Fastur! Hætti og skanna...")
    stop()
    time.sleep(1.0)

    # Bakka ef pláss er að aftan
    rear = min_distance(snapshot, zone_c)
    if rear > 40:
        print(f"Bakka ({rear:.0f}cm)...")
        send_speeds(-speed, -speed)
        time.sleep(0.5)
        stop()
        time.sleep(1.0)
    else:
        print(f"Aftur lokað ({rear:.0f}cm), sleppir bakki.")

    # Skanna og snúa í bestu átt
    snapshot = get_snapshot()
    heading, direction = findExit(snapshot)
    turnToExit(heading, direction)

    # Keyra beint áfram þar til hindrun kemur í sjón
    print("Keyri beint til að losna...")
    deadline = time.time() + 2.0
    while time.time() < deadline:
        fresh = get_snapshot()
        if min_distance(fresh, zone_a_narrow) <= start_turn:
            break
        send_speeds(speed, speed)
        time.sleep(0.05)
    stop()
    print("Komst út.")

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

            FrontClose = under(snapshot, zone_a_wide, start_turn)
            FrontStop  = front_dist <= sd  # uses min_distance from wide zone — catches thin objects
            RightClose = under(snapshot, zone_b, sd)
            LeftClose  = under(snapshot, zone_d, sd)

            right_clear = min_distance(snapshot, zone_b)
            left_clear  = min_distance(snapshot, zone_d)
            front_dist  = min_distance(snapshot, zone_a_wide)       # nálægasta hindrun framundan

            recent_fronts.append(front_dist)  # fylgjast með hreyfingu

            print(f"front: {front_dist:.0f}cm  FrontClose: {FrontClose}  FrontStop: {FrontStop}  L: {LeftClose}  R: {RightClose}")

            if is_stuck():
                # ------ Fastur — finna útveg ------
                print("Fastur! Skanna fyrir útveg...")
                escape_stuck(snapshot)

            elif not FrontStop and not FrontClose:
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
                    # Allt lokað — finna útveg
                    escape_stuck(snapshot)

            time.sleep(0.1)

    finally:
        stop_lidar()  # Stoppar LiDAR þegar autopilot hættir