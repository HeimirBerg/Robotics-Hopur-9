# skynjun

import time
from smbus import SMBus
from adafruit_servokit import ServoKit
import random

kit = ServoKit(channels=8)
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

    if current_value1 < 15:   # Skilgreinum ekkert endurkast sem 10
        current_value1 = 10
    if current_value2 < 15:
        current_value2 = 10

    if current_value1 < 15 and last1 < 50:      # Eih bull sem ég skil ekki sjálfur
        current_value1 = 10
        print("of nálægt")
    elif current_value1 < 15 and last1 >= 50:
        current_value1 = last1
        print("langt")
    if current_value2 < 15 and last2 < 50:         
        current_value2 = 10
        print("of nálægt")
    elif current_value1 < 15 and last2 >= 50:
        current_value1 = last2
        print("langt")
    
    last1 = current_value1
    last2 = current_value2

    print(f"Skynjari 1: {current_value1} cm    Skynjari 2: {current_value2} cm")
    return last1, last2

def hlutfall(merki1, merki2):
    if merki1 < 100 or merki2 < 100: # Notum fallið ef fjarlægð frá hlut er undir 100cm
        pass
    if merki1 == merki2: # Hér finnum við svo hlutfallið milli fjarlægðanna og hvor þeirra er lengra frá hindrun.
        hlutf = 1
        lengri = 0
    elif merki1 > merki2:
        hlutf = merki1/merki2
        lengri = 1
    elif merki1 < merki2:
        hlutf = merki2/merki1
        lengri = 2
    return hlutf, lengri
    
def hlidar(skyn1, skyn2): # Þetta fall er ætlað til þess að finna hvert á að beygja ef við lendum á hindrun
    kit.servo[0].angle = 45
    kit.servo[1].angle = 145
    time.sleep(1)  # Gefum örmum tíma til að hreyfa sig áður en við tökum mælingu
    x = sense(skyn1, skyn2)
    finnatt = hlutfall(x[0], x[1])
    if finnatt[1] == 0:
        uttak = random.randint(1,2)
    elif finnatt[1] == 1:
        uttak =  1
    elif finnatt[1] == 2:
        uttak = 2
    kit.servo[0].angle = 145
    kit.servo[1].angle = 45
    time.sleep(1)
    return uttak 
    
def tekkv(skyn1, skyn2): # Skoðum hvort það sé hægt að beygja til vinstri
    kit.servo[0].angle = 145
    time.sleep(1)
    x = sense(skyn1, skyn2)
    plass = x[0]
    kit.servo[0].angle = 180
    if plass == 10:
        return False
    elif plass >= 100:
        return True
    
def tekkh(skyn1, skyn2): # Skoðum hvort það sé hægt að beygja til hægri
    kit.servo[1].angle = 45
    time.sleep(1)
    x = sense(skyn1, skyn2)
    plass = x[1]
    kit.servo[1].angle = 0
    if plass == 10:
        return False
    elif plass >= 100:
        return True


uskyn1 = 500
uskyn2 = 500
while True:
    sjon = sense(uskyn1,uskyn2)
    uskyn1 = sjon[0]
    uskyn2 = sjon[1]
