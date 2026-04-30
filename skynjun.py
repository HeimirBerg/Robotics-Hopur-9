import time
from smbus import SMBus

i2c_bus = SMBus(1)
i2c_address1 = 0x71
i2c_address2 = 0x72

def classify(val):
    if val == 0 or val > 550:
        return 800   # out of range
    elif val < 25:
        return 0     # too close
    return val

def skynjun():
    # Trigger sensor 1, wait, read it — then do sensor 2 separately
    i2c_bus.write_byte_data(i2c_address1, 0, 0x51)
    time.sleep(0.07)
    data1 = i2c_bus.read_i2c_block_data(i2c_address1, 0, 4)

    i2c_bus.write_byte_data(i2c_address2, 0, 0x51)
    time.sleep(0.07)
    data2 = i2c_bus.read_i2c_block_data(i2c_address2, 0, 4)

    val1 = data1[2] * 256 + data1[3]
    val2 = data2[2] * 256 + data2[3]

    return classify(val1), classify(val2)