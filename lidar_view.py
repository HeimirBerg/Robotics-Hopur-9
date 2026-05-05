import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rplidar import RPLidar
import threading


LIDAR_PORT = '/dev/ttyUSB1'
BAUDRATE = 1000000
MIN_QUALITY = 10

# --- Shared scan data ---
latest_angles = []
latest_dists = []
scan_lock = threading.Lock()

def scan_worker(lidar):
    for scan in lidar.iter_scans():
        angles = []
        dists = []
        for quality, angle, dist_mm in scan:
            if quality >= MIN_QUALITY and dist_mm > 0:
                angles.append(np.radians(angle))
                dists.append(dist_mm / 1000.0)  # mm -> metres
        with scan_lock:
            latest_angles.clear()
            latest_angles.extend(angles)
            latest_dists.clear()
            latest_dists.extend(dists)

# --- Set up plot ---
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='polar')
ax.set_theta_zero_location('N')   # 0° at top (forward)
ax.set_theta_direction(-1)        # clockwise
ax.set_rlim(0, 6)                 # max 6 metres
ax.set_title('RPLIDAR S2L - Live View', pad=20)
ax.set_facecolor('#0d0d0d')
fig.patch.set_facecolor('#1a1a1a')
ax.tick_params(colors='white')
ax.title.set_color('white')
ax.grid(color='#333333')

scatter = ax.scatter([], [], s=2, c='#00ff88', alpha=0.8)

# Highlight front zone (330° - 30°)
theta_front = np.radians(np.concatenate([np.arange(330, 360), np.arange(0, 31)]))
ax.fill_between(theta_front, 0, 6, alpha=0.05, color='red', label='Front zone')

def update(frame):
    with scan_lock:
        angles = list(latest_angles)
        dists = list(latest_dists)
    if angles:
        scatter.set_offsets(np.c_[angles, dists])
        # Colour points by distance: green=far, red=close
        colors = plt.cm.RdYlGn(np.clip(np.array(dists) / 4.0, 0, 1))
        scatter.set_color(colors)
    return scatter,

# --- Start LiDAR ---
print("Connecting to LiDAR...")
lidar = RPLidar(LIDAR_PORT, baudrate=BAUDRATE)
time.sleep(3)
t = threading.Thread(target=scan_worker, args=(lidar,), daemon=True)
t.start()
print("Running — close the window to stop.")

ani = animation.FuncAnimation(fig, update, interval=100, blit=False)

try:
    plt.show()
finally:
    lidar.stop()
    lidar.disconnect()
    print("Done.")