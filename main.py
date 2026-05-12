from manualdrive import manual
from auto import *
from movement import stop

try:
    while True:
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
            angle,distance = autopilot()
            print(f"Angle: {angle}, Distance: {distance}")
        elif adalval == 2:
            manual()
        elif adalval == 3:
            stop()
            break
        else:
            print("Vinsamlegast veldu gildandi tölu")
except KeyboardInterrupt:
    stop()
    print("\n-------- Ó fokk --------")