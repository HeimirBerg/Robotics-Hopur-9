import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

kit.servo[0].angle = 0
kit.servo[1].angle = 0
time.sleep(1)
kit.servo[0].angle = 180
kit.servo[1].angle = 0
time.sleep(1)
kit.servo[0].angle = 0
kit.servo[1].angle = 0
time.sleep(1) 
kit.servo[0].angle = 180
kit.servo[1].angle = 0
time.sleep(1) 
kit.servo[0].angle = None
kit.servo[1].angle = None
print("keyrt")