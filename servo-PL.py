import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

def servo_move():
    while True:
        # Hreyfing til hliðar
        for angle in range(0, 146):
            servo0_angle = 180 - angle
            servo1_angle = angle

            kit.servo[0].angle = servo0_angle
            kit.servo[1].angle = servo1_angle

            time.sleep(0.03)

            yield servo0_angle, servo1_angle

        # Hreyfing fram
        for angle in range(145, -1, -1):
            servo0_angle = 180 - angle
            servo1_angle = angle

            kit.servo[0].angle = servo0_angle
            kit.servo[1].angle = servo1_angle

            time.sleep(0.03)

            yield servo0_angle, servo1_angle


#for current_angle in servo_move():
    print("Current angle:", current_angle)