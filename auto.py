from skynjun import *
def autopilot():
    while True:
        s1, s2 = skynjun()
        print(f"Skynjari 1: {s1}, Skynjari 2: {s2}")
        if s1 and s2 == 0:
            pass #Stoppa
        elif s1 < 50:
            pass #beygja til hægri (skörp beygja)
        elif s2 < 50:
            pass #beyja til vinstri (skörp beygja)
        elif s1 < 100:
            pass #beygja til hægri (milli-skörp beygja)
        elif s2 < 100:
            pass #beyja til vinstri (milli-skörp beygja)
        elif s1 < 200:
            pass #beygja til hægri (álíðandi beygja)
        elif s2 < 200:
            pass #beyja til vinstri (álíðandi beygja)
        else:
            pass
