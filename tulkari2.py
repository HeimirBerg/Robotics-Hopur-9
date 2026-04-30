# skynjun

import time
from smbus import SMBus

i2c_bus = SMBus(1)
i2c_address1 = 0x71
i2c_address2 = 0x72

def sense():
    i2c_bus.write_byte_data(i2c_address1, 0, 0x51) # Mæli í cm
    i2c_bus.write_byte_data(i2c_address2, 0, 0x51)

    time.sleep(0.07)  # 70ms

    data1 = i2c_bus.read_i2c_block_data(i2c_address1, 0, 4) # Sjáum hvað ég fékk
    data2 = i2c_bus.read_i2c_block_data(i2c_address2, 0, 4)

    current_value1 = data1[2] * 256 + data1[3] # Reiknum saman hvað kom út
    current_value2 = data2[2] * 256 + data2[3]

    if current_value1 == 0:         # Skynjari túlkar ekkert endurkast sem 0, skilgreinum það sem seinasta
        current_value1 = last1
    if current_value2 == 0:
        current_value2 = last2
    
    if current_value1 == current_value2:
        hlutf = 1
        lengri = "jafnt"
    elif current_value1 > current_value2:
        hlutf = current_value1/current_value2
        lengri = "1 er stærri"
    elif current_value2 > current_value1:
        hlutf = current_value2/current_value1
        lengri = "2 er stærri"
    
    last1 = current_value1
    last2 = current_value2

    print(f"Skynjari 1: {current_value1} cm    Skynjari 2: {current_value2} cm      Hlutfall: {hlutf} {lengri}")
    return current_value1, current_value2, hlutf

def hlutfall(a,b):
    v = a/255
    h = b/255
    

while True:
    sjon = sense()
    if sjon [0] < 30 or sjon[1] < 30:
        print("Of nálægt")
    if sjon[0] == 17 and sjon[1] == 17:
        break