from pyrplidar import PyRPlidar
import threading
import time

LidarPort = "/dev/ttyUSB0"
Baudrate  = 1000000
MaxRange  = 300  # cm

ScanData = {}
Lock     = threading.Lock()
Running  = False
_thread  = None

def _scan_worker():
    global Running, ScanData
    lidar = PyRPlidar()
    try:
        lidar.connect(port=LidarPort, baudrate=Baudrate, timeout=3)
        lidar.reset()
        time.sleep(5)
        lidar.lidar_serial._serial.reset_input_buffer()

        scan_gen = None
        for attempt in range(100):
            try:
                scan_gen = lidar.start_scan()
                print(f"Scan started on attempt {attempt + 1}")
                break
            except Exception:
                time.sleep(0.05)

        if scan_gen is None:
            raise Exception("Could not start scan after 100 attempts")

        for scan in scan_gen():
            if not Running:
                break
            angle    = round(scan.angle) % 360
            distance = scan.distance / 10.0
            if 0 < distance <= MaxRange:
                with Lock:
                    ScanData[angle] = distance

    except Exception as e:
        print(f"LiDAR error: {e}")
    finally:
        Running = False
        lidar.stop()
        lidar.disconnect()
        print("LiDAR disconnected.")

def start_lidar():
    global Running, _thread
    Running = True
    _thread = threading.Thread(target=_scan_worker, daemon=True)
    _thread.start()
    time.sleep(8)  # Bíður eftir reset + fyrsta scan
    print("LiDAR ready.")

def stop_lidar():
    global Running
    Running = False
    if _thread:
        _thread.join(timeout=3)

def get_snapshot():
    with Lock:
        return dict(ScanData)

def under(snapshot, zone, threshold):
    for a, d in snapshot.items():
        if a in zone:
            if d < threshold:
                return True
    return False

def zone_clearance(snapshot, zone):
    distances = []
    for angle, dist in snapshot.items():
        if angle in zone:
            distances.append(dist)
    if distances:
        return sum(distances) / len(distances)
    else:
        return MaxRange

def min_distance(snapshot, zone):
    distances = []
    for angle, dist in snapshot.items():
        if angle in zone:
            distances.append(dist)
    if distances:
        return min(distances)
    else:
        return MaxRange