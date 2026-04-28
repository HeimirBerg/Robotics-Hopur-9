from skynjun import *
from hreyfing import *
while True:
    val = input("Veldu Átt(u,n,h,v eða 0 til að hætta: )")
    if val == u:
        print(fara_afram())
    elif val == n:
        print(fara_aftur())
    elif val == h:
        print(beyja("Hægri"))
    elif val == v:
        print(beyja("Vinstri"))
    elif val == 0:
        break
    else:
        print("villa")
