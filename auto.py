from sensor import *
from movement import *
from collections import deque
import time


# ------Fastar------
speed      = 200
start_turn = 130
sd         = 45

STUCK_THRESHOLD = 5   # cm — hversu lítil hreyfing telst fastur
STUCK_TIME      = 10  # fjöldi lestrar áður en við segjum að hann sé fastur
front_history   = deque(maxlen=5)

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

def is_stuck():
    if len(recent_fronts) < STUCK_TIME:
        return False
    # Fjarlægt bailout — hann getur verið fastur jafnvel þótt framundan sé opið
    return max(recent_fronts) - min(recent_fronts) < STUCK_THRESHOLD

def escape_stuck(snapshot):
    recent_fronts.clear()
    print("Fastur! Hætti og skanna...")
    stop()
    time.sleep(2.0)  # Bíður lengur — LiDAR þarf tíma til að fylla scan eftir stop

    # Fersk mynd eftir stop — eldri snapshot getur verið úrelt
    snapshot = get_snapshot()

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
    if direction is not None:
        turnToExit(heading, direction)
    else:
        # FIX 3: Neyðarúrræði — snúast 180° í stað þess að keyra beint í vegginn aftur
        print("Gat ekki fundið útveg — snýst 180° sem neyðarúrræði...")
        drive(255, 4, -1)  # snúast til hægri
        time.sleep(180 * degTime)
        stop()
        time.sleep(0.4)

    # Keyra beint áfram þar til hindrun kemur í sjón — nota vítt svæði til að grípa horn
    print("Keyri beint til að losna...")
    deadline = time.time() + 3.0
    while time.time() < deadline:
        fresh = get_snapshot()
        if min_distance(fresh, zone_a_wide) <= start_turn:
            break
        send_speeds(speed, speed)
        time.sleep(0.05)
    stop()
    print("Komst út.")

def findExit(snapshot):
    # FIX 1: Vantar lestur → MaxRange — opið rými (>300cm) er skýrt, ekki 80cm hindrun
    full = [snapshot.get(a, MaxRange) for a in range(360)]
    # Lágmark í glugga — tryggir að öll leiðin sé frjáls, ekki bara meðaltal
    # Meðaltal getur villst af nokkrum fjarlægum lesturum við brún veggjar
    min_in_window = [
        min(full[(a + i) % 360] for i in range(-15, 16))
        for a in range(360)
    ]

    if max(min_in_window) <= 80:
        # Snapshot of tæmt — vantar gögn til að finna útveg
        print(f"Snapshot of tæmt ({max(min_in_window):.0f}cm) — bíð eftir betri gögnum")
        return 0, None

    # Finna næsta horn við 0° með næga clearance — ekki þarf lengsta leið, bara næsta
    MIN_CLEARANCE = 100  # cm — lágmarkspláss til að teljast góður útveg

    def angular_dist(a):
        # Fjarlægð frá 0° (beint fram) — 180° er lengst í burtu
        return a if a <= 180 else 360 - a

    viable = [a for a in range(360) if min_in_window[a] >= MIN_CLEARANCE]

    if viable:
        best_angle = min(viable, key=angular_dist)  # Næsti útvegur, ekki stærsti
    else:
        # Enginn útvegur með næga clearance — velja opnasta horn sem fallback
        best_angle = max(range(360), key=lambda a: min_in_window[a])

    direction = "Hægri" if 1 <= best_angle <= 179 else "Vinstri"
    print(f"Best exit: {best_angle}° ({min_in_window[best_angle]:.0f}cm min) → {direction}")
    return best_angle, direction

def turnToExit(heading, direction):
    if direction == "Hægri":
        angle   = heading
        dir_num = 4
    else:
        angle   = 360 - heading
        dir_num = 3
    if angle < 2 or angle > 358:  # Nær beint á útveg — engin þörf á snúningi
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
            # FIX 2: Bíða eftir fullnægjandi scan (a.m.k. 180 horn) áður en við tökum ákvörðun
            for _ in range(10):
                snapshot = get_snapshot()
                if len(snapshot) >= 180:
                    break
                time.sleep(0.3)

            FrontClose = under(snapshot, zone_a_wide, start_turn)
            FrontStop = under(snapshot, zone_a_narrow, sd)  # Aðeins þröngt svæði — forðast rangar niðurstöður vegna þunna hluta eins og stólsfóta
            RightClose = under(snapshot, zone_b, sd)
            LeftClose  = under(snapshot, zone_d, sd)

            right_clear = min_distance(snapshot, zone_b)
            left_clear  = min_distance(snapshot, zone_d)
            front_dist  = min_distance(snapshot, zone_a_wide)       # nálægasta hindrun framundan

            front_history.append(front_dist)
            smoothed_front = sum(front_history) / len(front_history)
            recent_fronts.append(front_dist)  # fylgjast með hreyfingu — hrá gildi til að varðveita náttúrulega dreifni

            print(f"front: {front_dist:.0f}cm  FrontClose: {FrontClose}  FrontStop: {FrontStop}  L: {LeftClose}  R: {RightClose}")

            if not FrontStop and not FrontClose:
                # ------ keyra áfram ------
                if is_stuck():
                    # Fastur í opnu rými — hjólín snúast ekki — finna útveg
                    print("Fastur! Skanna fyrir útveg...")
                    escape_stuck(snapshot)
                else:
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

                # Bæta við horn-fjarlægðir svo hlutir í 30-44° blintu blettinum séu greindir
                corner_r_dist = min_distance(snapshot, zone_corner_r)
                corner_l_dist = min_distance(snapshot, zone_corner_l)
                effective_right = min(right_clear, corner_r_dist)
                effective_left  = min(left_clear,  corner_l_dist)

                if effective_left < effective_right:
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