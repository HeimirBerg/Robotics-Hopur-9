# skynjun

import time
from smbus import SMBus

i2c_bus = SMBus(1)
i2c_address1 = 0x71
i2c_address2 = 0x72

def sense():
    i2c_bus.write_byte_data(i2c_address1, 0, 0x51)
    i2c_bus.write_byte_data(i2c_address2, 0, 0x51)

    time.sleep(0.07)  # 70ms

    data1 = i2c_bus.read_i2c_block_data(i2c_address1, 0, 4)
    data2 = i2c_bus.read_i2c_block_data(i2c_address2, 0, 4)

    current_value1 = data1[2] * 256 + data1[3]
    current_value2 = data2[2] * 256 + data2[3]

    if current_value1 == 0:
        current_value1 = 255
    if current_value2 == 0:
        current_value2 = 255

    print(f"Skynjari 1: {current_value1} cm    Skynjari 2: {current_value2} cm")
    return current_value1, current_value2

while True:
    sjon = sense()
    if sjon[0] == 17 and sjon[1] == 17:
        break