from pyrplidar import PyRPlidar

lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=1000000, timeout=3)

lidar.start_motor()

scan_generator = lidar.start_scan()

for count, scan in enumerate(scan_generator()):
    print(count, scan)
    if count == 100:
        break

lidar.stop()
lidar.disconnect()