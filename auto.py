from skynjun2 import *
from servo import *
from hreyfing import *


def autopilot():
    s0, s1 = 200, 200
    hradi = 100
    while True:
        for servo0, servo1 in servo_move():
            s0, s1, merki = sense(s0, s1)
            dist = min(s0, s1)

            if merki == 1:              # of nálægt, snúa við
                beyja("Hægri", hradi, -hradi)
            elif dist < 100:            # að nálgast hindrun, byrja að beyja
                reikna_beyju(servo1, dist, hradi)
            else:                       # keyra áfram
                fara_afram(hradi)
