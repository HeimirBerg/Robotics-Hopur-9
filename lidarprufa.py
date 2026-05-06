from pyrplidar import PyRPlidar
import time

lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=1000000, timeout=3)
lidar.reset()
time.sleep(5)

# flush leftover reset bytes
for attr in ['_serial', 'serial', '_serial_port', 'serial_port', '_port', 'port']:
    if hasattr(lidar.lidar_serial, attr):
        getattr(lidar.lidar_serial, attr).reset_input_buffer()
        break

scan_gen = lidar.start_scan()

try:
    for scan in scan_gen():
        print(scan.angle, scan.distance)
except KeyboardInterrupt:
    lidar.stop()
    lidar.disconnect()