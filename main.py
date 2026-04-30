from skynjun import *
from hreyfing import *

hradi = velja_hrada()
print(hradi)
beyju_hradi = velja_radius(hradi)
print(beyju_hradi)
adalval = int(input(" Vinsamlegast veldu eftirfarandi:\n 1 - Autopilot\n 2 - Manual Mode\n 3 - Hætta\n "))
i = 1
while i == 1:
    if adalval == 1:
        s1,s2 = skynjun()
        print(f"Skynjari 1: {s1}, Skynjari 2: {s2}")
    elif adalval == 2:
        k = 1
        while k == 1:
            val = input("Veldu Átt(w,a,s,d eða 0 til að hætta): ")
            if val == "w":
                print(fara_afram(hradi))
            elif val == "s":
                print(fara_aftur(hradi))
            elif val == "d":
                print(beyja("Hægri",hradi,beyju_hradi))
            elif val == "a":
                print(beyja("Vinstri",hradi,beyju_hradi))
            elif val == "0":
                print(stoppa())
                break
            elif val == "f":
                print(velja_hrada())
            elif val == "r":
                print(velja_radius(hradi))
            else:
                print("villa")
    elif adalval == 0:
        break
    else:
        print("Vinsamlegast veldu gildandi tölu")
