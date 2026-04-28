import smbus
import time
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

def fara_afram():
    return senda(225,-225)
    
def fara_aftur():
    return senda(-225,225)

def beyja(att):
    if att == "Hægri":
        return senda(225,-100)

    elif att == "Vinstri":
        return senda(100,-225)
    else: 
        return "Villa! skrifaðu annað hvort \"Hægri\" eða \"Vinstri\""

def stoppa():
    return senda(0,0)




    
