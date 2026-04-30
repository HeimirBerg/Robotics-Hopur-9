import time
from smbus import SMBus

i2c_bus = SMBus(1)
i2c_address1 = 0x71
i2c_address2 = 0x72

def skynjun():
    last_value1 = 800
    last_value2 = 800

    
    i2c_bus.write_byte_data(i2c_address1, 0, 0x51)
    i2c_bus.write_byte_data(i2c_address2, 0, 0x51)

    time.sleep(0.07)  # 70ms

    data1 = i2c_bus.read_i2c_block_data(i2c_address1, 0, 4)
    data2 = i2c_bus.read_i2c_block_data(i2c_address2, 0, 4)

    current_value1 = data1[2] * 256 + data1[3]
    current_value2 = data2[2] * 256 + data2[3]

    if last_value1 < 20:
            current_value1 = 0
    elif last_value1 > 550:
            current_value1 = 800
    else:
        pass
    if last_value2 < 20:
        current_value2 = 0
    elif last_value1 > 550:
        current_value2 = 800
    else:
        pass
    last_value1 = current_value1
    last_value2 = current_value2

        


    return current_value1, current_value2