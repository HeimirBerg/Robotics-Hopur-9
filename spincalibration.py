from movement import drive, stop
import time

degTime = 1.0 / 36.3  # calculated from last run: 180° command → 182° actual at 1.0/35.9

TARGET_DEGREES = 180
duration = TARGET_DEGREES * degTime

print(f"Spinning RIGHT {TARGET_DEGREES}° — calculated duration: {duration:.3f}s")
print("Starting in 3 seconds... mark your heading now.")
time.sleep(3)

drive(255, 4, -1)
time.sleep(duration)
stop()

print("Done. Measure the actual angle turned and update degTime.")
print(f"  Formula: degTime = {duration:.4f} / actual_degrees")