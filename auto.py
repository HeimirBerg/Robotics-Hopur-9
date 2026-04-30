from skynjun import *
def autopilot():
    while True:
        s1, s2 = skynjun()
        print(f"Skynjari 1: {s1}, Skynjari 2: {s2}")
        if s1 and s2 == 0:
            pass #Stoppa
        elif s1 < 50