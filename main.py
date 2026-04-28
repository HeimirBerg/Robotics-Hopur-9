from skynjun import *
from hreyfing import *
while True:
    val = input("Veldu Átt(w,a,s,d eða 0 til að hætta): ")
    if val == "w":
        print(fara_afram())
    elif val == "s":
        print(fara_aftur())
    elif val == "d":
        print(beyja("Hægri"))
    elif val == "a":
        print(beyja("Vinstri"))
    elif val == "0":
        break
    else:
        print("villa")
