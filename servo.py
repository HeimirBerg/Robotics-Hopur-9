import time

from adafruit_servokit import ServoKit

# Initialize for 8 channels
kit = ServoKit(channels=8)


print("Moving to 90")
kit.servo[0].angle = 90
time.sleep(1)

