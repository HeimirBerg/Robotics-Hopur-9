import time
from rplidar import RPLidar

# --- Configuration ---
LIDAR_PORT = '/dev/ttyUSB0'
BAUDRATE = 1000000
TOO_CLOSE = 20      # cm - danger zone
MIN_QUALITY = 10

FRONT_ZONE = (330, 30)
LEFT_ZONE  = (30, 150)
RIGHT_ZONE = (210, 330)

_lidar = None
_scan_iter = None


def start_lidar():
    global _lidar, _scan_iter
    _lidar = RPLidar(LIDAR_PORT, baudrate=BAUDRATE)
    _scan_iter = _lidar.iter_scans()
    print("LiDAR ready")


def stop_lidar():
    if _lidar:
        _lidar.stop()
        _lidar.disconnect()


def _min_dist_in_zone(scan, angle_start, angle_end):
    distances = []
    for quality, angle, dist_mm in scan:
        if quality < MIN_QUALITY or dist_mm <= 0:
            continue
        if angle_start > angle_end:
            in_zone = angle >= angle_start or angle <= angle_end
        else:
            in_zone = angle_start <= angle <= angle_end
        if in_zone:
            distances.append(dist_mm / 10.0)
    return min(distances) if distances else 999


def sense(last1=200, last2=200):
    try:
        scan = next(_scan_iter)
    except Exception as e:
        print(f"Scan error: {e}")
        return last1, last2, 0

    front_dist = _min_dist_in_zone(scan, *FRONT_ZONE)
    left_dist  = _min_dist_in_zone(scan, *LEFT_ZONE)
    right_dist = _min_dist_in_zone(scan, *RIGHT_ZONE)

    s0 = min(left_dist, front_dist)
    s1 = min(right_dist, front_dist)

    if s0 <= 0 or s0 > 300:
        s0 = last1
    if s1 <= 0 or s1 > 300:
        s1 = last2

    merki = 1 if (front_dist < TOO_CLOSE or left_dist < TOO_CLOSE or right_dist < TOO_CLOSE) else 0

    return s0, s1, merki