import smbus
I2C_ADDRESS = 0x50   # Arduino slave address
bus = smbus.SMBus(1) # I2C bus on Pi Zero / Pi 3 / Pi 4

def senda(m1,m2):
    m1 = int(m1)
    m2 = int(m2)
    m1_sign  = 0 if m1 >= 0 else 1
    m2_sign  = 0 if m2 >= 0 else 1
    m1_speed = abs(m1)
    m2_speed = abs(m2)
    data = [m1_speed, m1_sign, m2_speed, m2_sign]
    bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)
    return f"Sent speeds → Motor1: {m1}, Motor2: {m2}"

def fara_afram(hradi):
    hradi = int(hradi)
    return senda(hradi,-hradi)
    
def fara_aftur(hradi):
    hradi = int(hradi)
    return senda(-hradi,hradi)

def beyja(att,hradi,radius):
    hradi = int(hradi)
    radius = int(radius)

    if att == "Hægri":
        return senda(hradi,-radius)

    elif att == "Vinstri":
        return senda(radius,-hradi)
    else: 
        return "Villa! skrifaðu annað hvort \"Hægri\" eða \"Vinstri\""

def stoppa():
    return senda(0,0)

def velja_hrada():
    
    while True:
        try:
            hradi = int(input("Veldu hraða [15-255]: "))

            if not (15 <= hradi <= 255):
                print("Ógilt val! Sláðu inn heiltölu á bilinu [15-255].")
                continue
            else:
                break

        except ValueError:
            print("Ógilt val! Sláðu inn heiltölu á bilinu [15-255].")
            continue

    return hradi

def velja_radius(hradi):

    hradi = int(hradi)

    print(" Veldu hversu krappa beygju á að taka:\n 1: Á staðnum\n 2: Kröpp\n 3: Milli-millistig\n 4: Millistig\n 5: Aflíðandi")

    while True:
        try:
            val = int(input("Val: "))

            if val == 1:
                radius = -hradi
                break
            elif val == 2:
                radius = 0
                break
            elif val == 3:
                radius = (hradi/2.5)
                break
            elif val == 4:
                radius = (hradi/1.9)
                break
            elif val == 5:
                radius = (hradi/1.3)
                break
            else:
                print("Ógilt val!")
                continue

        except ValueError:
            print("Ógilt val!")
            continue

    radius = int(radius)
    return radius


    
