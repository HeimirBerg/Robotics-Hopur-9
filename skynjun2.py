import time
from smbus import SMBus
from adafruit_servokit import ServoKit

i2c_bus = SMBus(1)
i2c_address1 = 0x71
i2c_address2 = 0x72

def sense(last1=200, last2=200):
    i2c_bus.write_byte_data(i2c_address1, 0, 0x51)
    time.sleep(0.1)
    data1 = i2c_bus.read_i2c_block_data(i2c_address1, 0, 4)

    i2c_bus.write_byte_data(i2c_address2, 0, 0x51)
    time.sleep(0.1)
    data2 = i2c_bus.read_i2c_block_data(i2c_address2, 0, 4)

    current_value1 = data1[2] * 256 + data1[3]
    current_value2 = data2[2] * 256 + data2[3]

    # Replace bad readings with last known good value
    if current_value1 == 0 or current_value1 > 300:
        current_value1 = last1
    if current_value2 == 0 or current_value2 > 300:
        current_value2 = last2

    sign = 0
    if current_value1 < 20 or current_value2 < 20:
        sign = 1  # too close
    elif current_value1 > 200 and current_value2 > 200:
        sign = 2  # too far

    return current_value1, current_value2, sign