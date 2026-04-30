# skynjun

import time
import threading
from smbus import SMBus

i2c_bus = SMBus(1)
i2c_address1 = 0x71
i2c_address2 = 0x72

def sense(last1,last2):
    i2c_bus.write_byte_data(i2c_address1, 0, 0x51) # Mæli í cm
    time.sleep(0.07)  # 70ms
    i2c_bus.write_byte_data(i2c_address2, 0, 0x51)
    time.sleep(0.07)  # 70ms 

    data1 = i2c_bus.read_i2c_block_data(i2c_address1, 0, 4) # Sjáum hvað ég fékk
    data2 = i2c_bus.read_i2c_block_data(i2c_address2, 0, 4)

    current_value1 = data1[2] * 256 + data1[3] # Reiknum saman hvað kom út
    current_value2 = data2[2] * 256 + data2[3]

    if current_value1 < 20:
        current_value1 = 1
    if current_value2 < 20:
        current_value2 = 1

    if current_value1 < 20 and last1 < 50:         # Skynjari túlkar ekkert endurkast sem 0, skilgreinum það sem seinasta
        current_value1 = last1
        print("of nálægt")
    elif current_value1 < 20 and last1 > 500:
        current_value1 = last1
        print("langt")
    if current_value2 < 20 and last2 < 50:         
        current_value2 = last2
        print("of nálægt")
    elif current_value1 < 20 and last2 > 500:
        current_value1 = last2
        print("langt")

    if current_value1 == current_value2:
        hlutf = 1
        lengri = "jafnt"
    elif current_value1 > current_value2:
        hlutf = round(current_value1/current_value2, 4)
        lengri = "1 er stærri"
    elif current_value2 > current_value1:
        hlutf = round(current_value2/current_value1, 4)
        lengri = "2 er stærri"
    
    last1 = current_value1
    last2 = current_value2

    print(f"Skynjari 1: {current_value1} cm    Skynjari 2: {current_value2} cm      Hlutfall: {hlutf} {lengri}")
    return last1, last2, hlutf

def hlutfall(a,b):
    v = a/255
    h = b/255
    
uskyn1 = 500
uskyn2 = 500

while True:
    sjon = sense(uskyn1,uskyn2)
    uskyn1 = sjon[0]
    uskyn2 = sjon[1]


    