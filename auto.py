from skynjun import *
from servo import *
def autopilot():
    while True:
        servo0, servo1 = servo_move()
        #s0, s1 = skynjun()

        print(f"servo 0: {servo0},  Servo 1: {servo1}")
        
