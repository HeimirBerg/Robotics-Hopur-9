def LiDAR_data():
    global _running
    lidar = PyRPlidar()
    lidar.connect(port=LIDAR_PORT, baudrate=BAUDRATE, timeout=3)
    lidar.reset()
    time.sleep(5)
    lidar.lidar_serial._serial.reset_input_buffer()

    scan_gen = lidar.start_scan()
    _running = True  # ← add this

    for scan in scan_gen():
        if not _running:
            break
        angle    = round(scan.angle) % 360
        distance = scan.distance / 10.0
        with _lock:
            _scan_data[angle] = distance
        print(f"Angle: {angle}°, Distance: {distance:.1f} cm")  # optional

    lidar.stop()
    lidar.disconnect()