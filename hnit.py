import math
import time
from movement import *
from lidarprufa import get_distance, start_lidar, stop_lidar

# --- Stillingar ---
SPEED = 255
CM_PER_SEC = 40.0  # Mælingin þín: 40cm á 1 sekúndu
GOAL_X = 200.0     # Markmið X (t.d. 2 metrar til hægri)
GOAL_Y = 300.0     # Markmið Y (t.d. 3 metrar áfram)

class RobotPos:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0  # 0 gráður er beint áfram (Y-ás)

    def update(self, dt, speed_val):
        """Reiknar ný hnit byggt á hraða og tíma."""
        if speed_val == 0: return
        
        dist = CM_PER_SEC * dt
        # Breytum gráðum í radíana fyrir math föllin
        rad = math.radians(self.heading)
        
        # Uppfærum X og Y
        self.x += dist * math.sin(rad)
        self.y += dist * math.cos(rad)

def drive_to_coordinates(target_x, target_y):
    pos = RobotPos()
    start_lidar()
    last_time = time.time()
    
    print(f"Keyri á hnit: ({target_x}, {target_y})")

    try:
        while True:
            # 1. Tímataka
            now = time.time()
            dt = now - last_time
            last_time = now

            # 2. Reikna fjarlægð og horn í markmið
            dx = target_x - pos.x
            dy = target_y - pos.y
            dist_to_goal = math.sqrt(dx**2 + dy**2)
            
            # Stopper ef við erum komnir innan við 10cm frá markmiði
            if dist_to_goal < 10:
                print("Komin á áfangastað!")
                break

            # Reikna hvaða átt við eigum að snúa í (Target Heading)
            target_heading = math.degrees(math.atan2(dx, dy)) % 360
            
            # 3. Athuga hindranir með LiDAR
            front = get_distance(345, 15)
            
            if front < 40:
                # HINDRUN: Forgangur hjá öryggiskerfi
                print(f"Hindrun ({front:.0f}cm)! Sveigja frá...")
                stop()
                # Hér gætir þú sett 'escape_stuck()' fallið þitt
                # Eftir beygjuna verður þú að uppfæra pos.heading!
                time.sleep(0.5) 
                
            else:
                # LEIÐRÉTTING: Snúa bílnum í átt að markmiði
                angle_diff = (target_heading - pos.heading + 180) % 360 - 180
                
                if abs(angle_diff) > 10:
                    # Snúa á staðnum ef hornið er vitlaust
                    print(f"Leiðrétti stefnu: {pos.heading:.1f}° -> {target_heading:.1f}°")
                    if angle_diff > 0:
                        drive(255, 4, -1) # Snúa hægri
                    else:
                        drive(255, 3, -1) # Snúa vinstri
                    
                    # Uppfæra áttina byggt á SEC_PER_DEG fastanum þínum
                    # (Hér þarf að vita hversu mikið hann snýst á dt sekúndum)
                    pos.heading += angle_diff * 0.1 # Einfölduð uppfærsla
                else:
                    # Keyra áfram og uppfæra staðsetningu
                    forward(SPEED)
                    pos.update(dt, SPEED)

            print(f"Staða: ({pos.x:.1f}, {pos.y:.1f}) | Eftir: {dist_to_goal:.1f}cm")
            time.sleep(0.1)

    finally:
        stop()
        stop_lidar()

# Keyra forritið
drive_to_coordinates(GOAL_X, GOAL_Y)