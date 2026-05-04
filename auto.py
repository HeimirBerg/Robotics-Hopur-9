from skynjun import *
from servo import *
def autopilot():
    while True:
        servo0, servo1 = servo_move()
        s0, s1 = skynjun()
        
        print(f"Skynjari 1: {s1}, Skynjari 2: {s2}")
        
