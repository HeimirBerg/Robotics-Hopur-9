import smbus
import time
bus = smbus.SMBus(1)
address = 0x70  # upphaflega addressan
next_address = 0xE2  # næsta address, nota 0xE2 til að fá 0x71


def write(value):
    bus.write_byte_data(address, 0, value)
    return -1


write(0xA0)
write(0xAA)
write(0xA5)
write(next_address)

time.sleep(0.7)
