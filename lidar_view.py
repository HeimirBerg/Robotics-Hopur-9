import threading
import math
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from pyrplidar import PyRPlidar

# --- Configuration ---
LIDAR_PORT = "/dev/ttyUSB0"
BAUDRATE = 1000000
MOTOR_PWM = 660       # Motor speed (0-1023), 660 is default
MAX_DISTANCE = 8000   # Max display distance in mm (8 metres)

# --- Shared scan data ---
scan_data = {"angles": [], "distances": []}
data_lock = threading.Lock()
running = True

# --- LiDAR setup ---
lidar = PyRPlidar()

def scan_worker():
    global running
    try:
        lidar.connect(port=LIDAR_PORT, baudrate=BAUDRATE, timeout=3)
        print("Connected to LiDAR...")
        lidar.reset()
        time.sleep(5)  # Wait for reset and motor spin up

        # Flush the serial buffer before starting scan
        serial_port = None
        for attr in ['_serial', 'serial', '_serial_port', 'serial_port', '_port', 'port']:
            if hasattr(lidar.lidar_serial, attr):
                serial_port = getattr(lidar.lidar_serial, attr)
                print(f"Found serial port at attribute: {attr}")
                break
        if serial_port:
            serial_port.reset_input_buffer()
            print("Buffer flushed.")
        else:
            print(f"Could not find serial port. Attributes: {dir(lidar.lidar_serial)}")

        scan_generator = lidar.start_scan()
        print("Scan started!")

        angles = []
        distances = []

        for scan in scan_generator():
            if not running:
                break

            angle = scan.angle
            distance = scan.distance

            if distance > 0:
                angles.append(math.radians(angle))
                distances.append(distance)

            # When we complete a full rotation, update shared data
            if scan.start_flag and len(angles) > 0:
                with data_lock:
                    scan_data["angles"] = list(angles)
                    scan_data["distances"] = list(distances)
                angles = []
                distances = []

    except Exception as e:
        print(f"LiDAR error: {e}")
    finally:
        try:
            lidar.stop()
            lidar.disconnect()
            print("LiDAR disconnected.")
        except Exception:
            pass

# --- Matplotlib polar plot ---
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location("N")   # 0 degrees at top (North)
ax.set_theta_direction(-1)         # Clockwise (like a compass)
ax.set_ylim(0, MAX_DISTANCE)
ax.set_title("RPLIDAR S2L — Live View", va="bottom")
ax.grid(True)

scatter = ax.scatter([], [], s=2, c="lime", alpha=0.8)

def update(frame):
    with data_lock:
        angles = list(scan_data["angles"])
        distances = list(scan_data["distances"])

    if angles and distances:
        scatter.set_offsets(np.column_stack((angles, distances)))
        # Colour points by distance (closer = brighter)
        scatter.set_array(np.array(distances))
        scatter.set_cmap("plasma")
        scatter.set_clim(0, MAX_DISTANCE)
    return (scatter,)

def on_close(event):
    global running
    running = False

fig.canvas.mpl_connect("close_event", on_close)

# --- Start scan thread ---
thread = threading.Thread(target=scan_worker, daemon=True)
thread.start()
print("Running — close the window to stop.")

ani = animation.FuncAnimation(
    fig, update, interval=100, blit=False, cache_frame_data=False
)

plt.show()
running = False
thread.join(timeout=3)