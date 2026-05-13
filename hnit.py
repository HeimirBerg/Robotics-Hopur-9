import math
import time
from movement import *
from lidarprufa import get_distance, start_lidar, stop_lidar, get_scan_snapshot
from lidar_auto import find_escape_heading, spin_to_heading, SEC_PER_DEG_AT_255

# --- Stillingar ---
SPEED = 255
CM_PER_SEC = 40.0 
# Inntak í mm breytt í cm til að passa við LiDAR gögn
GOAL_X = float(input("Sláðu inn vegalengd til hliðar í cm (+hægri-vinstri): ")) 
GOAL_Y = float(input("Sláðu inn færslu áfram í cm: ")) 

class RobotPos:
    def __init__(self): # Upphafsstillum staðsetningu og stefnu
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0 

    def update(self, dt, speed_val): # Finnur breytingu á staðsetningu
        if speed_val == 0: return
        dist = CM_PER_SEC * dt
        rad = math.radians(self.heading)
        self.x += dist * math.sin(rad)
        self.y += dist * math.cos(rad)

def drive_to_coordinates(target_x, target_y): # Keyrum á ákveðin hnit
    pos = RobotPos() # Staðsetning
    start_lidar() # Kveikir á lidar
    last_time = time.time()
    
    print(f"Keyri á hnit: ({target_x}, {target_y})")

    try:
        while True:
            now = time.time()
            dt = now - last_time
            last_time = now

            dx = target_x - pos.x
            dy = target_y - pos.y
            dist_to_goal = math.sqrt(dx**2 + dy**2)
            
            if dist_to_goal < 10:
                print("Komin á áfangastað!")
                break

            target_heading = math.degrees(math.atan2(dx, dy)) % 360
            
            # 1. Athuga hindranir
            front = get_distance(330, 30)
            
            if front < 70:
                print(f"HINDRUN ({front:.0f}cm)! Leita að leið framhjá...")
                stop()
                
                snapshot = get_scan_snapshot() # Gögn úr lidar
                best_angle, turn_dir = find_escape_heading(snapshot) # Finnum hvert á að beygja
                
                # Snúa bílnum í átt að opna svæðinu
                spin_to_heading(best_angle, turn_dir)
                
                # UPPFÆRA STEFNU: Núna veit Navigatorinn hvert nefið snýr
                pos.heading = best_angle
                
                # Keyra smá áfram til að hreinsa hindrunina áður en við reynum við hnitin aftur
                forward(SPEED)
                time.sleep(0.8)
                stop()
                
            else:
                # 2. LEIÐRÉTTING: Snúa í átt að markmiði
                angle_diff = (target_heading - pos.heading + 180) % 360 - 180
                
                if abs(angle_diff) > 10:
                    # Snúa á staðnum
                    dir_num = 4 if angle_diff > 0 else 3
                    # Reikna tíma byggt á nákvæma kalíberingunni þinni
                    turn_duration = abs(angle_diff) * SEC_PER_DEG_AT_255
                    
                    drive(255, dir_num, -1)
                    time.sleep(turn_duration)
                    stop()
                    
                    # Uppfæra heading eftir snúninginn
                    pos.heading = target_heading
                else:
                    # Keyra áfram og uppfæra staðsetningu
                    forward(SPEED)
                    pos.update(dt, SPEED)

            print(f"Staða: ({pos.x:.1f}, {pos.y:.1f}) | Stefna: {pos.heading:.1f}° | Eftir: {dist_to_goal:.1f}cm")
            time.sleep(0.05)

    finally:
        stop()
        stop_lidar()

drive_to_coordinates(GOAL_X, GOAL_Y)