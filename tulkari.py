import time
from smbus import SMBus

i2c_bus = SMBus(1)
i2c_address1 = 0x71
i2c_address2 = 0x72

while 1:
    i2c_bus.write_byte_data(i2c_address1, 0, 0x51)  # Tell sensor to scan in mm
    i2c_bus.write_byte_data(i2c_address2, 0, 0x51)  # Tell sensor to scan in mm

    time.sleep(0.05)  # Bíða eftir bylgjunni

    high1 = i2c_bus.read_byte_data(i2c_address1, 2)  # Read the high byte of the value
    #print(high) # print the value of High byte
    high2 = i2c_bus.read_byte_data(i2c_address2, 2)  # Read the high byte of the value
    #print(high) # print the value of High byte

    low1 = i2c_bus.read_byte_data(i2c_address1, 3)  # Read the low byte of the value
    #print(low) # print the value of low byte
    low2 = i2c_bus.read_byte_data(i2c_address2, 3)  # Read the low byte of the value
    #print(low) # print the value of low byte

    current_value1 = high1 * 256 + low1 
    current_value2 = high2 * 256 + low2

    print(f"skynjari 1: {current_value1}    Skynjari 2: {current_value2}")

    