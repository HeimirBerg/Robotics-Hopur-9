from sensor import *
from movement import *
from collections import deque
import time


# ------Fastar------
speed      = 200
start_turn = 130
sd         = 50

STUCK_THRESHOLD = 5   # cm — hversu lítil hreyfing telst fastur
STUCK_TIME      = 20  # fjöldi lestrar áður en við segjum að hann sé fastur
front_history   = deque(maxlen=5)  # ← add this

DRIFT_THRESHOLD = 5   # cm — hversu lítil breyting í lestri þegar keyrt er beint
DRIFT_COUNT     = 20  # fjöldi lestrar — hversu lengi við fylgjumst með áður en við segjum fastur

# ------ Svæði ------
zone_a_wide   = set(range(315, 360)) | set(range(0, 46))  # Fram — vítt — snemma uppgötvun (±45°)
zone_a_narrow = set(range(345, 360)) | set(range(0, 16))  # Fram — þröngt — beint framundan
zone_b = set(range(45, 136))                               # Hægri
zone_c = set(range(135, 226))                              # Aftur
zone_d = set(range(225, 316))                              # Vinstri
zone_corner_r = set(range(30, 70))                         # Framhægri horn
zone_corner_l = set(range(290, 330))                       # Framvinstri horn
corner_sd     = 60                                         # cm — byrja að beygja þegar horn nálgast hlut
degTime = 3.0 / 64.8                                      # Tíma fasti til að snúa bílnum

recent_fronts = deque(maxlen=STUCK_TIME)
recent_all    = deque(maxlen=DRIFT_COUNT)  # fylgjast með lestrum óháð fjarlægð — grípur kyrrstöðu á opnum svæðum

def is_stuck():
    if len(recent_fronts) < STUCK_TIME:
        return False
    if min(recent_fronts) > start_turn:  # allar lestur frjálsar — ekki fastur
        return False
    return max(recent_fronts) - min(recent_fronts) < STUCK_THRESHOLD

def is_drifting_stuck():
    # Virkar jafnvel þegar lestur er yfir start_turn — grípur kyrrstöðu á opnum svæðum
    # þar sem is_stuck() sér ekki neitt vegna þess að allar lestur eru "frjálsar"
    if len(recent_all) < DRIFT_COUNT:
        return False
    return max(recent_all) - min(recent_all) < DRIFT_THRESHOLD

def escape_stuck(snapshot):
    recent_fronts.clear()
    recent_all.clear()  # hreinsa drift-sögu líka svo hann fari ekki strax í escape aftur
    print("Fastur! Hætti og skanna...")
    stop()
    time.sleep(1.0)

    # Bakka ef pláss er að aftan
    rear = min_distance(snapshot, zone_c)
    if rear > 40:
        print(f"Bakka ({rear:.0f}cm)...")
        send_speeds(-speed, -speed)
        time.sleep(1.0)
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
    deadline = time.time() + 3.0
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
    # Lágmark í glugga — tryggir að öll leiðin sé frjáls, ekki bara meðaltal
    # Meðaltal getur villst af nokkrum fjarlægum lesturum við brún veggjar
    min_in_window = [
        min(full[(a + i) % 360] for i in range(-15, 16))
        for a in range(360)
    ]
    best_angle = max(range(360), key=lambda a: min_in_window[a])
    direction  = "Hægri" if 1 <= best_angle <= 179 else "Vinstri"
    print(f"Best exit: {best_angle}° ({min_in_window[best_angle]:.0f}cm min) → {direction}")
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
            FrontStop = under(snapshot, zone_a_narrow, sd)  # Aðeins þröngt svæði — forðast rangar niðurstöður vegna þunna hluta eins og stólsfóta
            RightClose = under(snapshot, zone_b, sd)
            LeftClose  = under(snapshot, zone_d, sd)

            right_clear = min_distance(snapshot, zone_b)
            left_clear  = min_distance(snapshot, zone_d)
            front_dist  = min_distance(snapshot, zone_a_wide)       # nálægasta hindrun framundan

            front_history.append(front_dist)
            smoothed_front = sum(front_history) / len(front_history)
            recent_fronts.append(smoothed_front)  # fylgjast með hreyfingu
            recent_all.append(front_dist)          # hráar lestur — fyrir drift-greiningu

            print(f"front: {front_dist:.0f}cm  FrontClose: {FrontClose}  FrontStop: {FrontStop}  L: {LeftClose}  R: {RightClose}")

            if is_stuck() or is_drifting_stuck():
                # ------ Fastur — finna útveg ------
                print("Fastur! Skanna fyrir útveg...")
                escape_stuck(snapshot)

            elif not FrontStop and not FrontClose:
                # ------ keyra áfram ------
                CornerRightClose = under(snapshot, zone_corner_r, corner_sd)  # Framhægri horn nálægt
                CornerLeftClose  = under(snapshot, zone_corner_l, corner_sd)  # Framvinstri horn nálægt

                if LeftClose and not RightClose:
                    auto_calculate_turn("Hægri", front_dist, speed)   # Smávegis til hægri á meðan við keyrum áfram
                elif RightClose and not LeftClose:
                    auto_calculate_turn("Vinstri", front_dist, speed)  # Smávegis til vinstri á meðan við keyrum áfram
                elif CornerRightClose and not CornerLeftClose:
                    auto_calculate_turn("Vinstri", front_dist, speed)  # Horn hægri nálægt — beygja smávegis til vinstri
                elif CornerLeftClose and not CornerRightClose:
                    auto_calculate_turn("Hægri", front_dist, speed)   # Horn vinstri nálægt — beygja smávegis til hægri
                else:
                    send_speeds(speed, speed)  # Keyra beint áfram

            elif FrontClose and not FrontStop:
                # ------ Eitthvað framundan en enn pláss — róleg beygja ------
                front_ref = min(
                    min_distance(snapshot, zone_a_wide),
                    min_distance(snapshot, zone_a_narrow)
                )
                ratio = max(0.0, min(1.0, (front_ref - sd) / (start_turn - sd)))
                inner = int(speed * ratio)
                if left_clear < right_clear:
                    turn("Hægri", speed, inner)    # Beygja smá til hægri
                else:
                    turn("Vinstri", speed, inner)  # Beygja smá til vinstri

            elif FrontStop:
                # Stoppa og skanna alltaf — tryggir að hann finni útveg
                # jafnvel í U-laga rými þar sem hliðarveggir eru ekki nærri
                escape_stuck(snapshot)

            time.sleep(0.1)

    finally:
        stop_lidar()  # Stoppar LiDAR þegar autopilot hættir