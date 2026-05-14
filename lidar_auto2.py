from lidarprufa import start_lidar, stop_lidar, get_distance, get_scan_snapshot, MAX_RANGE
from movement import *

import time
import math
from collections import deque

# --- Fastar ---
speed         = 225
turn_distance = 150  # cm — start turning (increased so robot gets more distance to complete turns)
stop_distance = 30   # cm — stop and spin in place
STUCK_THRESHOLD = 3  # cm — how little movement counts as stuck
STUCK_TIME      = 15 # how many readings before declaring stuck
CLEAR_TIMEOUT   = 40 # loops — declare stuck if front hasn't cleared in this many cycles

ROBOT_WIDTH     = 18.5  # cm — physical width of robot
ROBOT_LENGTH    = 32.3  # cm — physical length of robot
ESCAPE_MARGIN   = 10    # cm — extra clearance on each side when looking for a gap

# Angular half-width the smoothing window must cover so a "clear" direction
# actually fits the robot at turn_distance range.
# arcsin((half_width + margin) / turn_distance), rounded up to nearest degree.
ESCAPE_WINDOW = math.ceil(
    math.degrees(math.asin((ROBOT_WIDTH / 2 + ESCAPE_MARGIN) / turn_distance))
)

# Calibration: how long drive(255, dir, -1) takes to spin 1° in place.
# To recalibrate: run drive(255, 4, -1) for exactly 1.0 s, measure the degrees
# turned, then set SEC_PER_DEG_AT_255 = 1.0 / measured_degrees.
# Current value is tuned for ~90° escape turns — adjust if over/under-shooting.
SEC_PER_DEG_AT_255 = 1.0 / 36.3   # calibrated: 180° command → 180° actual on new body

recent_fronts  = deque(maxlen=STUCK_TIME)
_loops_blocked = 0  # counts consecutive loops where front hasn't cleared turn_distance


def is_stuck():
    if len(recent_fronts) < STUCK_TIME:
        return False
    if min(recent_fronts) > turn_distance:  # all readings clear — not stuck
        return False
    return max(recent_fronts) - min(recent_fronts) < STUCK_THRESHOLD


def find_escape_heading(snapshot):
    """
    Find the most open direction in a 360° scan.

    Smooths each angle over a ±15° window so LiDAR noise spikes don't
    skew the result, then returns the angle with the highest average clearance.
    Always returns a result — never None.

    Returns (heading_angle, turn_direction).
    """
    full = [snapshot.get(a, MAX_RANGE) for a in range(360)]

    smoothed = [
        sum(full[(a + i) % 360] for i in range(-ESCAPE_WINDOW, ESCAPE_WINDOW + 1)) / (2 * ESCAPE_WINDOW + 1)
        for a in range(360)
    ]

    best_angle = max(range(360), key=lambda a: smoothed[a])
    direction  = "Hægri" if 1 <= best_angle <= 179 else "Vinstri"

    print(f"  Best escape heading: {best_angle}° ({smoothed[best_angle]:.0f}cm avg) → {direction}")
    return best_angle, direction


def spin_to_heading(heading, direction):
    """
    Spin on the spot at speed 255 to face a target heading using timed rotation.
    Uses drive(255, dir, -1) — turn_stage -1 = Á staðnum (spin in place).

    heading   : angle in degrees as returned by find_escape_heading
                (1–179 = Hægri side, 181–359 = Vinstri side, 0 = straight ahead)
    direction : "Hægri" or "Vinstri"

    Timing formula (always at speed 255):
        duration = angle × SEC_PER_DEG_AT_255
    """
    if direction == "Hægri":
        angle   = heading        # 1–179°
        dir_num = 4
    else:
        angle   = 360 - heading  # 181–359° → equivalent left-turn angle (1–179°)
        dir_num = 3

    if angle < 2:
        print("  Already facing the gap, no spin needed.")
        return

    duration = angle * SEC_PER_DEG_AT_255
    print(f"  Spinning {direction} {angle}° → {duration:.3f}s")
    drive(255, dir_num, -1)
    time.sleep(duration)
    stop()
    time.sleep(0.4)   # settle before handing back to main loop


def escape_stuck(left, right):
    """
    Stop, optionally back up, take a stationary 360° scan, calculate the
    exact spin needed to face the most open direction, then verify before
    handing back to the main loop.

    If the robot did not turn far enough (front still blocked after spin),
    re-scan and spin again — up to MAX_SPIN_RETRIES times — so that an
    under-powered or high-friction drivetrain gets extra chances to clear.
    """
    global _loops_blocked
    MAX_SPIN_RETRIES = 3   # max number of scan-and-spin attempts before giving up

    recent_fronts.clear()
    _loops_blocked = 0

    print("Stuck! Stopping for 360° scan...")
    stop()
    time.sleep(1.0)   # let LiDAR settle while stationary

    # Back up if there is room behind
    rear = get_distance(135, 225)
    if rear > 40:
        print(f"Backing up (rear: {rear:.0f}cm)...")
        reverse(speed)
        time.sleep(0.5)
        stop()
        time.sleep(1.0)
    else:
        print(f"Rear blocked ({rear:.0f}cm), skipping backup.")

    # Scan and spin to most open direction, retrying if the robot didn't turn far enough.
    # Each retry re-scans from wherever the robot actually ended up, so the heading
    # is always calculated from the current real position rather than the original one.
    for attempt in range(1, MAX_SPIN_RETRIES + 1):
        snapshot          = get_scan_snapshot()
        heading, turn_dir = find_escape_heading(snapshot)
        spin_to_heading(heading, turn_dir)

        front = get_distance(345, 15)
        print(f"  Post-spin front: {front:.0f}cm  (attempt {attempt}/{MAX_SPIN_RETRIES})")

        if front > turn_distance:
            break  # clear — proceed to drive out

        if attempt < MAX_SPIN_RETRIES:
            print("  Still blocked, re-scanning and spinning again...")
        else:
            print("  Could not clear after retries — stopping, will retry next cycle.")
            stop()
            return

    # Drive straight until a new obstacle comes into range, ignoring side sensors.
    # Uses narrow sensor so side walls don't abort the exit drive early.
    print("  Driving straight to clear the area...")
    deadline = time.time() + 2.0   # safety cap — max 2 s of straight driving
    while time.time() < deadline:
        if get_distance(345, 15) <= turn_distance:
            break
        forward(speed)
        time.sleep(0.05)
    stop()
    print("  Escape complete.")


def autopilot_prufa():
    global _loops_blocked
    start_lidar()
    print("Autopilot running.")

    try:
        while True:
            front_wide   = get_distance(315, 45)   # ±45° — early wall detection
            front_narrow = get_distance(345, 15)   # ±15° — dead ahead only
            right        = get_distance(45, 135)
            left         = get_distance(225, 315)

            recent_fronts.append(front_narrow)

            # Track how long the front has been blocked — catches oscillating readings
            # that fool is_stuck() into thinking the robot is moving
            if front_narrow < turn_distance:
                _loops_blocked += 1
            else:
                _loops_blocked = 0

            print(f"front: {front_narrow:.0f} ({front_wide:.0f} wide)  left: {left:.0f}  right: {right:.0f}  blocked: {_loops_blocked}")

            if is_stuck() or _loops_blocked >= CLEAR_TIMEOUT:
                print("Stuck! Scanning for escape route...")
                escape_stuck(left, right)

            elif front_wide > turn_distance:
                # Both sensors clear — drive straight at full speed
                forward(speed)

            elif front_narrow > stop_distance:
                # Wall detected — curve away smoothly like a car.
                # Outer wheel stays at full speed always.
                # Inner wheel slows with a squared ratio: more aggressive turning early on.
                front_ref = min(front_wide, front_narrow)
                ratio = ((front_ref - stop_distance) / (turn_distance - stop_distance)) ** 2  # squared for more aggressive early turning
                inner = int(speed * ratio)
                if left > right:
                    turn("Vinstri", speed, inner)
                else:
                    turn("Hægri", speed, inner)

            else:
                # Narrow sensor critically close — full escape
                print(f"Too close ({front_narrow:.0f}cm) — scanning for best heading...")
                escape_stuck(left, right)

            time.sleep(0.1)

    finally:
        stop_lidar()