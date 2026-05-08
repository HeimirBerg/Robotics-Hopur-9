"""
Spin calibration test — turns the robot 180° using the current
SEC_PER_DEG_AT_255 constant so you can see how much it actually turns.

Run:  python3 calibrate_spin.py
Mark the robot's starting heading, let it spin, then measure the real angle.
Update SEC_PER_DEG_AT_255 in lidar_auto.py accordingly:
    SEC_PER_DEG_AT_255 = 1.0 / (actual_degrees / 1.0)
    or more precisely: SEC_PER_DEG_AT_255 = duration / actual_degrees
"""

from movement import drive, stop
import time

# Must match the value in lidar_auto.py
SEC_PER_DEG_AT_255 = 1.0 / 170.8

TARGET_DEGREES = 180
duration = TARGET_DEGREES * SEC_PER_DEG_AT_255

print(f"Spinning RIGHT {TARGET_DEGREES}° — calculated duration: {duration:.3f}s")
print("Starting in 3 seconds... mark your heading now.")
time.sleep(3)

drive(255, 4, -1)   # Hægri, spin in place
time.sleep(duration)
stop()

print("Done. Measure the actual angle turned and update SEC_PER_DEG_AT_255.")
print(f"  Formula: SEC_PER_DEG_AT_255 = {duration:.4f} / actual_degrees")