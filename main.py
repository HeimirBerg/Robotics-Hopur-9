from skynjun import *
from hreyfing import *
from manual import *

while True:
    adalval = int(input(" Vinsamlegast veldu eftirfarandi:\n 1 - Autopilot\n 2 - Manual Mode\n 3 - Hætta\n "))
    if adalval == 1:
        try:
            while True:
                s1, s2 = skynjun()
                print(f"Skynjari 1: {s1}, Skynjari 2: {s2}")
        except KeyboardInterrupt:
            print("\nHætt við autopilot")
    elif adalval == 2:
        manual()
    elif adalval == 3:
        stoppa()
        break
    else:
        print("Vinsamlegast veldu gildandi tölu")