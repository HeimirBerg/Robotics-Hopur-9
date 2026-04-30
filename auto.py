from skynjun import *
def autopilot():
    while True:
        s1, s2,hf,stor = skynjun()
        print(f"Skynjari 1: {s1}, Skynjari 2: {s2}")
        if s1 and s2 == 0:
            pass #Stoppa og snúa við
        elif s1 < 20:
            pass #beygja til hægri (beygja á staðnum)
        elif s2 < 20:
            pass #beyja til vinstri (beygja á staðnum)
        elif s1 < 40:
            pass #beygja til hægri (milli-skörp beygja)
        elif s2 < 40:
            pass #beyja til vinstri (milli-skörp beygja)
        elif s1 < 60:
            pass #beygja til hægri (álíðandi beygja)
        elif s2 < 60:
            pass #beyja til vinstri (álíðandi beygja)
        else:
            pass
