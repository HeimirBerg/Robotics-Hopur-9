from skynjun import *
from hreyfing import *

val = input("Veldu Átt(u,n,h,v)")
if val == u:
    print(fara_afram())
elif val == n:
    print(fara_aftur())
elif val == h:
    print(beyja("Hægri"))
elif val == v:
    print(beyja("Vinstri"))
else:
    print("villa")
