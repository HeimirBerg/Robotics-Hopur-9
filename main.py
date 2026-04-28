from skynjun import *
from hreyfing import *
i = 1
while i == 1:
    val = input("Veldu Átt(w,a,s,d eða 0 til að hætta): ")
    if val == "w":
        print(fara_afram())
    elif val == "s":
        print(fara_aftur())
    elif val == "d":
        print(beyja("Hægri"))
    elif val == "a":
        print(beyja("Vinstri"))
    elif val == "stop":
        print(stoppa())
        break
    else:
        print("villa")
