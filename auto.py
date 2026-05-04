from skynjun2 import *
from servo import *
from hreyfing import *


def autopilot():
    s0, s1 = 200, 200
    hradi = 50
    while True:
        for servo0, servo1 in servo_move():
            s0, s1, merki = sense(s0, s1)

            if merki == 1:
                # allt of nálægt og snúa á staðnum
                beyja("Hægri", hradi, -hradi)

            elif s0 > 100 and s1 > 100:
                # keyra áfram
                fara_afram(hradi)

            elif s0 > 100 and s1 <= 100:
                radius = int(hradi * (s1 - 20) / 80)
                beyja("Hægri", hradi, max(0, radius))

            elif s1 > 100 and s0 <= 100:
                radius = int(hradi * (s0 - 20) / 80)
                beyja("Vinstri", hradi, max(0, radius))

            else:
                # both blocked - spin on the spot
                beyja("Hægri", hradi, -hradi)
