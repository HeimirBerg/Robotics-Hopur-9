import time
from smbus import SMBus

i2c_bus = SMBus(1)
i2c_address1 = 0x71
i2c_address2 = 0x72

def skynjun():
    i2c_bus.write_byte_data(i2c_address1, 0, 0x51)
    i2c_bus.write_byte_data(i2c_address2, 0, 0x51)

    time.sleep(0.07)  # 70ms

    data1 = i2c_bus.read_i2c_block_data(i2c_address1, 0, 4)
    data2 = i2c_bus.read_i2c_block_data(i2c_address2, 0, 4)

    current_value1 = data1[2] * 256 + data1[3]
    current_value2 = data2[2] * 256 + data2[3]

    # Sensor 1: 0 = too close, 800 = out of range, else = distance in cm
    if current_value1 == 0 or current_value1 > 550:
        current_value1 = 800  # out of range / too far
    elif current_value1 < 20:
        current_value1 = 0    # too close

    # Sensor 2: same logic
    if current_value2 == 0 or current_value2 > 550:
        current_value2 = 800  # out of range / too far
    elif current_value2 < 20:
        current_value2 = 0    # too close

    return current_value1, current_value2