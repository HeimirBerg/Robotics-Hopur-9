from sensor import *
from movement import *
from collections import deque
import time


# ------ Fastar ------
speed      = 200 # Hraði sem mótorar keyra á 0-255
start_turn = 130 # Byrja að beygja 130cm frá hindrun en samt bara rólega
sd         = 40  # sd stendur fyrir "Stop Distance" og er til staðar sem neyðarstopp. 
cornerSD     = 40 # Neyðarstopp fyrir hornin á róbotinum

StuckRange    = 5  # Hvenær róbot telst fastur. Ef að hann fær tölur +-5cm þá veit hann að hann sé fastur
StuckTime     = 20 # fjöldi gagna áður en við segjum að hann sé fastur
FrontHistory  = deque(maxlen=5) # Heldur utan um síðustu 5 mælingar að framan
SecondStuckRange = 8   # Auka stilling til að stilla hvenær hann er fastur. Ef að hann fær tölur +-8cm þá veit hann að hann sé fastur
SecondStuckTime     = 25  # Auka stilling yfir fjödla gagna sem að hann safnar til að vita að hann sé fastur
RecentFront = deque(maxlen=StuckTime)      # Heldur utan um síðustu 20 mælingar. Notað af fyrri fasta kerfinu
SecondRecentFront    = deque(maxlen=SecondStuckTime) # Heldur utan um síðustu 25 mælingar. Notað af seinni fasta kerfinu

# ------ LiDAR svæði ------
zone_a_wide   = set(range(315, 360)) | set(range(0, 46))  # Framsjón
zone_a_narrow = set(range(345, 360)) | set(range(0, 16))  # Þrengri framsjón
zone_b = set(range(45, 136))                               # Hægri
zone_c = set(range(135, 226))                              # Aftur
zone_d = set(range(225, 316))                              # Vinstri
zone_corner_r = set(range(30, 70))                         # Framhægri horn
zone_corner_l = set(range(290, 330))                       # Framvinstri horn
degTime = 1.0 / 17.1                                     # Tíma fasti til að snúa bílnum


# ------ Uppsetning falla sem að verða notaðar í Autopilot() ------
def Stuck(): # Skilgreinir hvenær róbotinn er fastur
    if len(RecentFront) < StuckTime: #Ekki nógu mikið af gögnum. hínkrað eftir fleiri mælingum
        return False
    if min(RecentFront) > start_turn:  # ef að allar mælingarnar eru langt frá þá er hann ekki fastur
        return False
    return max(RecentFront) - min(RecentFront) < StuckRange # Ef að mælingarnar breytast minna en StuckRange þá er hann fastur

def SecondStuck():
    # Virkar jafnvel þegar lestur er yfir start_turn — grípur kyrrstöðu á opnum svæðum
    # þar sem Stuck() sér ekki neitt vegna þess að allar lestur eru "frjálsar"
    # Notar þrönga lestur (zone_a_narrow) svo hliðarveggir kalli ekki á ranga greiningu
    if len(SecondRecentFront) < SecondStuckTime:
        return False
    return max(SecondRecentFront) - min(SecondRecentFront) < SecondStuckRange

def EscapeStuck(snapshot): 
    # Kallað á þegar að róbotinn er fastur. þá Stoppar, bakkar, finnur hann leið út og keyrir þangað
    RecentFront.clear()        # Hreinsar gögn svo hann haldi ekki að hann sé fastur
    SecondRecentFront.clear()  # Hreinsar gögn svo hann haldi ekki að hann sé fastur
    print("Fastur! Hætti og skanna...") # Prenta út að hann sé fastur 
    stop() # Stoppar róbotinn svo hann haldi ekki áfram að keyra
    time.sleep(1.0) # Smá seinkunn til að rugla ekki forritið

    # Bakkar ef pláss er að aftan
    rear = MinDistance(snapshot, zone_c) # Kalla á gögnin að aftan
    if rear > 40: # Ef pláss er að aftan (yfir 40cm) þá bakkar hann
        print(f"Bakka ({rear:.0f}cm)...")
        send_speeds(-speed, -speed)
        time.sleep(1.0)
        stop()
        time.sleep(1.0)
    else:
        # Ef að það er ekki pláss að aftan þá sleppir hann því að bakka
        print(f"Aftur lokað ({rear:.0f}cm), sleppir bakki.") 

    # Skanna og snúa í bestu átt mögulegt til að komast frá hindrun
    snapshot = GetSnapshot() # Tekur nýja mynd af umhverfinu eftir að hann hefur stoppað
    heading, direction = findExit(snapshot) # Finnur bestu leið til að komast út
    turnToExit(heading, direction) # Snýr í þá átt
    print("Keyri beint til að losna...")

    deadline = time.time() + 3.0 # Gefur sér 3 sekúndur til að losna
    while time.time() < deadline:
        fresh = GetSnapshot()
        if MinDistance(fresh, zone_a_narrow) <= start_turn: # Ef að hann lendir í hindrun, þá stoppar hann
            break
        send_speeds(speed, speed)
        time.sleep(0.05)
    stop()
    print("Komst út.")

def findExit(snapshot): # Skoðar umhverfið og finnur bestu leið út
    full = [snapshot.get(a, MaxRange) for a in range(360)]  # Sækir fjarlægð í hverri gráðu og ef að enginn mæling finnst í 
                                                            # þeirri gráðu er MaxRange notað í staðin
    min_in_window = []
    for a in range(360):
        window = [full[(a + i) % 360] for i in range(-15, 16)]  # 30 gráðu gluggi umhverfis í hverri gráðu
        min_in_window.append(min(window))  # Lágmarksfjarlægð í glugganum

    best_angle = max(range(360), key=lambda a: min_in_window[a])  # Finnur gráðuna með mesta pláss
    direction  = "Hægri" if 1 <= best_angle <= 179 else "Vinstri"  # Velur átt. Annað hvort hægri eða vinstri
    print(f"Best exit: {best_angle}° ({min_in_window[best_angle]:.0f}cm min) → {direction}") 
    return best_angle, direction  # Skilar bestu gráðu og stefnu til þess að fara í

def turnToExit(heading, direction): #Snýr bílnum í átt að útgangi
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



# ------ Aðal Autopilot Keyrslan ------
def autopilot():
    StartLidar()  # Byrjar LiDAR svo að hann keyri í bakgrunninum
    print("Autopilot running.") # Prenta stöðunni á honum
    try:
        while True:
            snapshot = GetSnapshot() # Tekur mynd af umhverfinu með LiDAR

            # Athuga hvort að það sé hindrun undir lágmarki í öllum svæðum
            FrontClose = under(snapshot, zone_a_wide, start_turn)
            FrontStop  = under(snapshot, zone_a_narrow, sd)  
            RightClose = under(snapshot, zone_b, sd)
            LeftClose  = under(snapshot, zone_d, sd)

            # Finna næstu hindrun á hliðunum
            right_clear = MinDistance(snapshot, zone_b)
            left_clear  = MinDistance(snapshot, zone_d)

            # Finna hindranir að framan
            front_dist_narrow = MinDistance(snapshot, zone_a_narrow)
            front_dist_wide   = MinDistance(snapshot, zone_a_wide)   

            # Skrá niður síðustu mælingar 
            FrontHistory.append(front_dist_narrow)
            SFront = sum(FrontHistory) / len(FrontHistory)
            RecentFront.append(SFront)  
            SecondRecentFront.append(front_dist_narrow)   

            print(f"front: {front_dist_narrow:.0f}cm  FrontClose: {FrontClose}  FrontStop: {FrontStop}  L: {LeftClose}  R: {RightClose}")

            # Ef að hann er fastur þá þarf hann að finna leið út
            if Stuck() == True or SecondStuck() == True:
                # ------ Fastur — finna útveg ------
                print("Fastur! Skanna fyrir útveg...")
                EscapeStuck(snapshot)
            
            
            elif FrontStop == False and FrontClose == False:
            # Ef að engin hindrun er fyrir framan. Keyra þá bara áfram
                CornerRightClose = under(snapshot, zone_corner_r, cornerSD)  # Athuga hvort að fram hægri hornið sé nálægt
                CornerLeftClose  = under(snapshot, zone_corner_l, cornerSD)  # Athuga hvort að fram vinstri hornið sé nálægt

                if LeftClose == True and RightClose == False:
                    auto_calculate_turn("Hægri", front_dist_narrow, speed)    # Ef að hindrun er vinstra megin en ekki hægra megin þá beygja til hægri
                elif RightClose == True and LeftClose == False:
                    auto_calculate_turn("Vinstri", front_dist_narrow, speed)  # Ef að hindrun er hægra megin en ekki vinstra megin þá beygja til vinstri
                elif CornerRightClose == True and CornerLeftClose == False:
                    auto_calculate_turn("Vinstri", front_dist_narrow, speed)  # Ef að hindrun er á hægra horni. Beygja þá til vinstri
                elif CornerLeftClose == True and CornerRightClose == False:
                    auto_calculate_turn("Hægri", front_dist_narrow, speed)    # Ef að hindrun er á vinstri horni. Beygja þá til hægri 
                else:
                    send_speeds(speed, speed)  # Engar hindranir á hliðunum. Keyra bara beint áfram

            elif FrontClose == True and FrontStop == False:
            #Ef að það er hindrun framundan en ekki alveg upp við. byrja að beygja smá
                front_ref = min(front_dist_wide, front_dist_narrow)
                ratio = max(0.0, min(1.0, (front_ref - sd) / (start_turn - sd)))
                inner = int(speed * ratio)
                if left_clear < right_clear:
                    turn("Hægri", speed, inner)    # Beygja smá til hægri
                else:
                    turn("Vinstri", speed, inner)  # Beygja smá til vinstri

            elif FrontStop == True:
                #Finna leið út
                EscapeStuck(snapshot)

            time.sleep(0.1)

    finally:
        StopLidar()  # Stoppar LiDAR þegar autopilot hættir