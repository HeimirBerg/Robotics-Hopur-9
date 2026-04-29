import time
from smbus import SMBus

i2c_bus = SMBus(1)
i2c_address2 = 0x71
i2c_address = 0x72

while 1:
    i2c_bus.write_byte_data(i2c_address, 0, 0x51)  # Tell sensor to scan in mm

    time.sleep(0.05)  # Bíða eftir bylgjunni

    high = i2c_bus.read_byte_data(i2c_address, 2)  # Read the high byte of the value
    #print(high) # print the value of High byte

    low = i2c_bus.read_byte_data(i2c_address, 3)  # Read the low byte of the value
    #print(low) # print the value of low byte

    current_value = high * 256 + low 

    print(current_value)

    