from manual import *
from auto import *

try:
    while True:
        adalval = int(input(" Vinsamlegast veldu eftirfarandi:\n 1 - Autopilot\n 2 - Manual Mode\n 3 - Hætta\n "))
        if adalval == 1:
            n = input("Enable Servo? Y/N: ")
            if n == "Y":
                autopilot()
            elif n == "N":
                autopilot(False)
            else:
                print("Error: pick Y/N: ")
        elif adalval == 2:
            manual()
        elif adalval == 3:
            stoppa()
            break
        else:
            print("Vinsamlegast veldu gildandi tölu")
except KeyboardInterrupt:
    stoppa()
    print("\n-------- Ó fokk --------")