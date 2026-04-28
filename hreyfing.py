import smbus
import time
I2C_ADDRESS = 0x50   # Arduino slave address
bus = smbus.SMBus(1) # I2C bus on Pi Zero / Pi 3 / Pi 4


def fara_afram():
    m1 = int(255)
    m2 = int(-255)
    m1_sign  = 0 if m1 >= 0 else 1
    m2_sign  = 0 if m2 >= 0 else 1
    m1_speed = abs(m1)
    m2_speed = abs(m2)
    data = [m1_speed, m1_sign, m2_speed, m2_sign]
    bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)
    return f"Sent speeds → Motor1: {m1}, Motor2: {m2}"
    
def fara_aftur():
    m1 = int(-255)
    m2 = int(255)
    m1_sign  = 0 if m1 >= 0 else 1
    m2_sign  = 0 if m2 >= 0 else 1
    m1_speed = abs(m1)
    m2_speed = abs(m2)
    data = [m1_speed, m1_sign, m2_speed, m2_sign]
    bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)
    return f"Sent speeds → Motor1: {m1}, Motor2: {m2}"

def beyja(att):
    if att == "Hægri":
        m1 = int(255)
        m2 = int(-100)
        m1_sign  = 0 if m1 >= 0 else 1
        m2_sign  = 0 if m2 >= 0 else 1
        m1_speed = abs(m1)
        m2_speed = abs(m2)
        data = [m1_speed, m1_sign, m2_speed, m2_sign]
        bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)
        return f"Sent speeds → Motor1: {m1}, Motor2: {m2}"

    elif att == "Vinstri":
        m1 = int(100)
        m2 = int(-255)
        m1_sign  = 0 if m1 >= 0 else 1
        m2_sign  = 0 if m2 >= 0 else 1
        m1_speed = abs(m1)
        m2_speed = abs(m2)
        data = [m1_speed, m1_sign, m2_speed, m2_sign]
        bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)
        print(f"Sent speeds → Motor1: {m1}, Motor2: {m2}")
    else: 
        return "Villa! skrifaðu annað hvort \"Hægri\" eða \"Vinstri\""

def stoppa():
    m1 = int(abs(0))
    m2 = int(abs(0))
    m1_sign  = 0 if m1 >= 0 else 1
    m2_sign  = 0 if m2 >= 0 else 1
    m1_speed = abs(m1)
    m2_speed = abs(m2)
    data = [m1_speed, m1_sign, m2_speed, m2_sign]
    bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)
    return f"Sent speeds → Motor1: {m1}, Motor2: {m2}"




    
