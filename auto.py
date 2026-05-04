from skynjun import *
from servo import *

def autopilot():
    s0, s1 = 200,200
    while True:
        for servo0, servo1 in servo_move():
            s0, s1,merki = sense(s0,s1)
            
            print(f"Skynjari 0: {s0},  Skynjari 1: {s1}, Merki: {merki}")
        
