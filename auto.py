from skynjun import *
from servo import *
def autopilot():
    while True:
        for servo0, servo1 in servo_move():
            s0, s1 = sense()

            print(f"Skynjari 0: {s0},  Skynjari 1: {s1}")
        
