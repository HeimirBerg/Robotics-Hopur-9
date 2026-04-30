from hreyfing import * 
def manual():
    hradi = velja_hrada()
    beyju_hradi = velja_radius(hradi)
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
            hradi = velja_hrada()       # save it back
            print(hradi)
        elif val == "r":
            beyju_hradi = velja_radius(hradi)   # save it back
            print(beyju_hradi)
        else:
            print("villa")