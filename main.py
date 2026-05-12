from manualdrive import manual
from auto import *
from movement import stop
import subprocess

try:
    """subprocess.Popen("python3 myndavel.py")""" # Keyrir myndavél í bakgrunni
    while True: # Fyrst veljum við hvernig stillingu við ætlum að hafa á róbótanum
        adalval = int(input(" Vinsamlegast veldu eftirfarandi:\n 1 - Autopilot\n 2 - Manual Mode\n 3 - Hætta\n "))
        if adalval == 1: 
            '''
            n = input("Enable Servo? Y/N: ")
            if n == "Y":
                autopilot()
            elif n == "N":
                autopilot(False)
            else:
                print("Error: pick Y/N: ")
                '''
            autopilot()
        elif adalval == 2:
            manual() # Við stjórnum róbótanum með fjarstýringu
        elif adalval == 3:
            stop() # Stoppum forritið
            break
        else:
            print("Vinsamlegast veldu gilda tölu")
except KeyboardInterrupt:
    stop()
    print("\n-------- Ó fokk --------")