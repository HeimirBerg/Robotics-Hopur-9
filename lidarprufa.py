from pyrplidar import PyRPlidar
import time


def scan():
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=1000000, timeout=3)
    lidar.lidar_serial.set_dtr(False)  # enables motor on S2L
    time.sleep(1)

    scan_gen = lidar.start_scan()
    

    try:
        for scan in scan_gen():
            angle = scan.angle
            distance = scan.distance
            return angle, distance
    except KeyboardInterrupt:
        lidar.lidar_serial.set_dtr(True)
        lidar.stop()
        lidar.disconnect()




'''
lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=1000000, timeout=3)
lidar.lidar_serial.set_dtr(False)  # enables motor on S2L
time.sleep(1)

scan_gen = lidar.start_scan()

try:
    for scan in scan_gen():
        print(scan.angle, scan.distance)
except KeyboardInterrupt:
    lidar.lidar_serial.set_dtr(True)
    lidar.stop()
    lidar.disconnect()

    '''