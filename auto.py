from skynjun2 import *
from servo import *
from hreyfing import *


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
                beygja("Hægri", hradi, -hradi)

            elif s0 > 100 and s1 > 100:
                fara_afram(hradi)

            elif s0 > 100 and s1 <= 100:
                if servoenable:
                    reikna_beygju(servo0, s1, hradi, servoenable)
                else:
                    radius = int(hradi * (s1 - 20) / 80)
                    beygja("Vinstri", hradi, max(0, radius))

            elif s1 > 100 and s0 <= 100:
                if servoenable:
                    reikna_beygju(servo1, s0, hradi, servoenable)
                else:
                    radius = int(hradi * (s0 - 20) / 80)
                    beygja("Hægri", hradi, max(0, radius))

            else:
                beygja("Hægri", hradi, -hradi)

        if not servoenable:
            time.sleep(0.1)