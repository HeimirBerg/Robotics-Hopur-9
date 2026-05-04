from skynjun2 import *
from servo import *
from hreyfing import *


def autopilot(servoenable=True):
    s0, s1 = 200, 200
    hradi = 50
    while True:
        servo_iter = servo_move() if servoenable else [(90, 90)]

        for servo0, servo1 in servo_iter:
            s0, s1, merki = sense(s0, s1)

            if merki == 1:
                beygja("Hægri", hradi, -hradi)

            elif s0 > 100 and s1 > 100:
                fara_afram(hradi)

            elif s0 > 100 and s1 <= 100:
                reikna_beygju(servo0, s1, hradi, servoenable)

            elif s1 > 100 and s0 <= 100:
                reikna_beygju(servo1, s0, hradi, servoenable)

            else:
                beygja("Hægri", hradi, -hradi)