from sensor import *
from movement import *
import time
'''
# ------Fastar------
speed = 150
start_turn = 60
sd = 20 #Stop distance

zone_a = set(range(315, 360)) | set(range(0, 46))   # Fram
zone_b = set(range(45, 136))                        # Hægri
zone_c = set(range(135, 226))                       # Aftur
zone_d = set(range(225, 316))                       # Vinstri

def autopilot():
    #   Kalla á upplýsingar frá LiDAR
    for angle, distance in LiDAR_data():
        if angle in zone_a:
            # ------ Framsjón milli 315° og 45° ------
            if distance > start_turn:
                pass #Keyra áfram
            elif distance <= start_turn and distance > sd:
                #Byrja að beygja rólega frá hindrun
                if angle in zone_b or angle in zone_d: 
                    if distance < sd:
                        pass #Ekki beygja
            elif distance < sd:
                pass 
                # ------ Ef að hann kemst ekki áfram og er alveg upp að hlutinum ------
                # ------ Stoppa, horfa í kring. finna bestu leið og snúa þangað og halda áfram ------
            # ----------------------------------------

        if distance in zone_a < sd and (distance in zone_b < sd and distance in zone_d < sd):
            # Byrja að bakka
            pass
            '''
# ------Fastar------
speed      = 150
start_turn = 60
sd         = 20  # Stop distance

# ------ Svæði ------
zone_a = set(range(315, 360)) | set(range(0, 46))  # Fram
zone_b = set(range(45, 136))                        # Hægri
zone_c = set(range(135, 226))                       # Aftur
zone_d = set(range(225, 316))                       # Vinstri
def autopilot():
    for _, _ in LiDAR_data():  # keeps the lidar running
        snapshot = get_snapshot()
        print(snapshot)
        '''
        front_near  = any_under(snapshot, zone_a, start_turn)
        front_stop  = any_under(snapshot, zone_a, sd)
        right_block = any_under(snapshot, zone_b, sd)
        left_block  = any_under(snapshot, zone_d, sd)

        right_clear = zone_clearance(snapshot, zone_b)
        left_clear  = zone_clearance(snapshot, zone_d)

        if not front_stop and not front_near:
            # ------ keyra áfram ------
            if left_block and not right_block:
                pass  # Smávegis til hægri á meðan við keyrum áfram
            elif right_block and not left_block:
                pass  # Smávegis til vinstri á meðan við keyrum áfram
            else:
                pass  # Keyra beint áfram

        elif front_near and not front_stop:
            # ------ Eitthvað framundan en enn pláss — rólegt beyg ------
            if left_clear > right_clear:
                pass  # Beygja smávegis til vinstri
            else:
                pass  # Beygja smávegis til hægri

        elif front_stop:
            # ------ Of nálægt framundan — stoppa ------
            if not left_block and not right_block:
                if left_clear > right_clear:
                    pass  # Beygja til vinstri
                else:
                    pass  # Beygja til hægri
            elif left_block and right_block:
                # Allt lokað — bakka og beygja
                pass  # Bakka
                if left_clear > right_clear:
                    pass  # Beygja til vinstri eftir að bakka
                else:
                    pass  # Beygja til hægri eftir að bakka
            '''