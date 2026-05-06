from pyrplidar import PyRPlidar
import time
try:
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=1000000, timeout=3)
    lidar.set_motor_pwm(660)  # start the motor
    time.sleep(2)
    print("jo")
    scan_gen = lidar.start_scan()

    for scan in scan_gen():
        print(scan.angle)      # 0-360 degrees
        print(scan.distance)   # distance in mm (divide by 10 for cm)
        print(scan.start_flag) # True when a new rotation begins
except KeyboardInterrupt:
    lidar.set_motor_pwm(0)
    lidar.stop()
    lidar.disconnect()