from skynjun import *
from servo import *
def sense1():
    i2c_bus.write_byte_data(i2c_address1, 0, 0x51)
    time.sleep(0.07)
    data1 = i2c_bus.read_i2c_block_data(i2c_address1, 0, 4)

    i2c_bus.write_byte_data(i2c_address2, 0, 0x51)
    time.sleep(0.07)
    data2 = i2c_bus.read_i2c_block_data(i2c_address2, 0, 4)

    current_value1 = data1[2] * 256 + data1[3]
    current_value2 = data2[2] * 256 + data2[3]

    # Sensor 1
    if current_value1 == 0 or current_value1 > 200:
        current_value1 = 999   # too far / out of range
    elif current_value1 < 15:
        current_value1 = -1    # too close

    # Sensor 2
    if current_value2 == 0 or current_value2 > 200:
        current_value2 = 999   # too far / out of range
    elif current_value2 < 15:
        current_value2 = -1    # too close

    return current_value1, current_value2
def autopilot():
    while True:
        for servo0, servo1 in servo_move():
            s0, s1 = sense1()

            print(f"Skynjari 0: {s0},  Skynjari 1: {s1}")
        
