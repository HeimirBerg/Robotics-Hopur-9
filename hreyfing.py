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
    return senda(hradi,-hradi)
    
def fara_aftur(hradi):
    return senda(-hradi,hradi)

def beyja(att,hradi):
    if att == "Hægri":
        return senda(hradi,-(hradi/2.25))

    elif att == "Vinstri":
        return senda((hradi/2.25),-hradi)
    else: 
        return "Villa! skrifaðu annað hvort \"Hægri\" eða \"Vinstri\""

def stoppa():
    return senda(0,0)

def velja_hrada():
    gildi = -1
    while not (0 < gildi <= 255):
        try:
            gildi = int(input("Veldu hraða [1-255]: "))

            if not (0 < gildi <= 255):
                print("Villa! Sláðu inn heiltölu á bilinu [1-255].")
                continue
            else:
                hradi = gildi
                break

        except ValueError:
            print("Villa! Sláðu inn heiltölu á bilinu [1-255].")
            continue

    return hradi




    
