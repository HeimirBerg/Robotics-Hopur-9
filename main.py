from skynjun import *
from hreyfing import *

hradi = velja_hrada()

i = 1
while True:
    val = input("Veldu Átt(w,a,s,d eða 0 til að hætta): ")
    if val == "w":
        print(fara_afram(hradi))
    elif val == "s":
        print(fara_aftur(hradi))
    elif val == "d":
        print(beyja("Hægri",hradi))
    elif val == "a":
        print(beyja("Vinstri",hradi))
    elif val == "0":
        print(stoppa())
        break
    elif val == "r":
        velja_hrada()
    else:
        print("villa")
