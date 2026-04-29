from skynjun import *
from hreyfing import *

hradi = velja_hrada()
print(hradi)
beyju_hradi = velja_radius(hradi)
print(beyju_hradi)
while True:
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
