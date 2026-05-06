from pyrplidar import PyRPlidar
import time

lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=1000000, timeout=3)
lidar.stop()
lidar.set_motor_pwm(0)
time.sleep(1)
lidar.disconnect()