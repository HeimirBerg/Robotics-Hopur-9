from skynjun2 import *
from servo import *
from movement import *


import time

def autopilot(servoenable=True):
    s0, s1 = 200, 200
    hradi = 200
    while True:
        servo_iter = servo_move() if servoenable else [(90, 90)]

        for servo0, servo1 in servo_iter:
            try:
                s0, s1, merki = sense(s0, s1)
            except OSError:
                time.sleep(0.1)
                continue

            if merki == 1:
                turn("Hægri", hradi, -hradi)

            elif s0 > 100 and s1 > 100:
                forward(hradi)

            elif s0 > 100 and s1 <= 100:
                if servoenable:
                    auto_calculate_turn(servo0, s1, hradi)
                else:
                    radius = int(hradi * (s1 - 20) / 80)
                    turn("Vinstri", hradi, max(0, radius))

            elif s1 > 100 and s0 <= 100:
                if servoenable:
                    auto_calculate_turn(servo1, s0, hradi)
                else:
                    radius = int(hradi * (s0 - 20) / 80)
                    turn("Hægri", hradi, max(0, radius))

            else:
                turn("Hægri", hradi, -hradi)

        if not servoenable:
            time.sleep(0.1)