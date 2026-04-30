import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

kit.servo[0].angle = 45
kit.servo[1].angle = 90
kit.servo[0].angle = None
kit.servo[1].angle = None
print("keyrt")