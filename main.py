from manual import *
from auto import *

while True:
    adalval = int(input(" Vinsamlegast veldu eftirfarandi:\n 1 - Autopilot\n 2 - Manual Mode\n 3 - Hætta\n "))
    if adalval == 1:
        autopilot()
    elif adalval == 2:
        manual()
    elif adalval == 3:
        stoppa()
        break
    else:
        print("Vinsamlegast veldu gildandi tölu")