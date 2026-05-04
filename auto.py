from skynjun2 import *
from servo import *
from hreyfing import *


def autopilot():
    s0, s1 = 200, 200
    hradi = 150
    while True:
        for servo0, servo1 in servo_move():
            s0, s1, merki = sense(s0, s1)

            if merki == 1:
                
                beygja("Hægri", hradi, -hradi)

            elif s0 > 100 and s1 > 100:
                
                fara_afram(hradi)

            elif s0 > 100 and s1 <= 100:
                radius = int(hradi * (s1 - 20) / 80)
                if servo0 < 90:
                    beygja("Hægri", hradi, max(0, radius))
                else:
                    beygja("Vinstri", hradi, max(0, radius))

            elif s1 > 100 and s0 <= 100:
                radius = int(hradi * (s0 - 20) / 80)
                if servo1 < 90:
                    beygja("Hægri", hradi, max(0, radius))
                else:
                    beygja("Vinstri", hradi, max(0, radius))

            else:
                beygja("Hægri", hradi, -hradi)