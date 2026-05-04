from skynjun import *
from servo import *
def sense1():
    while True:
        i2c_bus.write_byte_data(i2c_address1, 0, 0x51)
        time.sleep(0.07)
        data1 = i2c_bus.read_i2c_block_data(i2c_address1, 0, 4)
        time.sleep(0.07)  # let the echo die out before firing sensor 2

        i2c_bus.write_byte_data(i2c_address2, 0, 0x51)
        time.sleep(0.07)
        data2 = i2c_bus.read_i2c_block_data(i2c_address2, 0, 4)

        raw1 = data1[2] * 256 + data1[3]
        raw2 = data2[2] * 256 + data2[3]

        return f"Raw 0: {raw1},  Raw 1: {raw2}"
        time.sleep(0.5)
def autopilot():
    while True:
        for servo0, servo1 in servo_move():
            #s0, s1 = sense1()
            print(sense1())
            #print(f"Skynjari 0: {s0},  Skynjari 1: {s1}")
        
