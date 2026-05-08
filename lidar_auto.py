from lidarprufa import start_lidar, stop_lidar, get_distance, get_scan_snapshot, MAX_RANGE
from hreyfing import *

import time
import math
from collections import deque

# --- Fastar ---
speed         = 150
turn_distance = 80   # cm — start turning
stop_distance = 20   # cm — stop and spin in place
STUCK_THRESHOLD = 3  # cm — how little movement counts as stuck
STUCK_TIME      = 15 # how many readings before declaring stuck

ROBOT_WIDTH     = 14.5  # cm — physical width of robot
ESCAPE_MARGIN   = 10    # cm — extra clearance on each side when looking for a gap
MIN_ESCAPE_DIST = 50    # cm — minimum distance to consider a direction clear

recent_fronts = deque(maxlen=STUCK_TIME)


def is_stuck():
    if len(recent_fronts) < STUCK_TIME:
        return False
    if min(recent_fronts) > turn_distance:  # all readings clear — not stuck
        return False
    return max(recent_fronts) - min(recent_fronts) < STUCK_THRESHOLD


def find_escape_heading(snapshot):
    """
    Scan all 360° and find the best heading to escape.
    Returns (heading_angle, turn_direction) or None if no gap found.

    A gap is valid if:
      - All readings within it are >= MIN_ESCAPE_DIST
      - Its physical width at the closest point fits the robot + margin
    """
    # Fill any missing angles with MAX_RANGE (open space)
    full = [snapshot.get(a, MAX_RANGE) for a in range(360)]

    # Find contiguous clear sectors, handling wrap-around by doubling the list
    clear = [d >= MIN_ESCAPE_DIST for d in full]
    clear2 = clear * 2

    gaps = []
    i = 0
    while i < 360:
        if clear2[i]:
            j = i
            while j < i + 360 and clear2[j]:
                j += 1
            length = j - i
            if length < 360:  # ignore if entire circle is clear (open field)
                gaps.append((i % 360, length))
            i = max(i + 1, j)
        else:
            i += 1

    if not gaps:
        print("No clear gaps found in 360° scan.")
        return None

    best_heading   = None
    best_direction = None
    best_score     = -1

    for start, length in gaps:
        center = (start + length // 2) % 360

        # Minimum distance anywhere inside this gap
        gap_angles = [(start + k) % 360 for k in range(length)]
        min_dist   = min(full[a] for a in gap_angles)

        # Physical width of the gap at that closest point (chord length formula)
        phys_width = 2 * min_dist * math.sin(math.radians(length / 2))

        needed = ROBOT_WIDTH + 2 * ESCAPE_MARGIN

        print(f"  Gap: start={start}° span={length}° min_dist={min_dist:.0f}cm width={phys_width:.0f}cm (need {needed:.0f}cm)")

        if phys_width >= needed:
            # Score: prefer gaps that are far away and wide
            score = min_dist * length
            if score > best_score:
                best_score     = score
                best_heading   = center
                # heading 1-179 = right side of robot, 181-359 = left side
                best_direction = "Hægri" if 1 <= center <= 179 else "Vinstri"

    if best_heading is not None:
        print(f"Best escape: {best_heading}° → turn {best_direction}")
    else:
        print("No gap wide enough for the robot.")

    return (best_heading, best_direction) if best_heading is not None else None


def escape_stuck(left, right):
    """Back up if safe, then spin toward the best escape gap."""
    recent_fronts.clear()
    stoppa()
    time.sleep(0.1)

    # Check rear clearance before reversing
    rear = get_distance(135, 225)
    if rear > 40:
        print(f"Backing up (rear: {rear:.0f}cm)...")
        fara_aftur(speed)
        time.sleep(0.5)
        stoppa()
        time.sleep(0.1)
    else:
        print(f"Rear blocked ({rear:.0f}cm), skipping backup.")

    # Full 360° scan to find the best way out
    snapshot = get_scan_snapshot()
    result   = find_escape_heading(snapshot)

    if result is None:
        # No usable gap — fall back to spinning toward the more open side
        print("Fallback: spinning toward more open side.")
        turn_dir = "Vinstri" if left > right else "Hægri"
    else:
        _, turn_dir = result

    print(f"Spinning {turn_dir} until front clears...")
    while get_distance(300, 60) <= turn_distance:
        beygja(turn_dir, speed, -speed)
        time.sleep(0.1)

    print("Escape complete.")


def autopilot():
    start_lidar()
    print("Autopilot running.")

    try:
        while True:
            front = get_distance(300, 60)
            right = get_distance(45, 135)
            left  = get_distance(225, 315)

            recent_fronts.append(front)

            print(f"front: {front:.0f}  left: {left:.0f}  right: {right:.0f}")

            if is_stuck():
                print("Stuck! Scanning for escape route...")
                escape_stuck(left, right)

            elif front > turn_distance:
                fara_afram(speed)

            elif front > stop_distance:
                # ratio: 1.0 when far away, 0.0 when at stop_distance
                ratio = (front - stop_distance) / (turn_distance - stop_distance)

                # Outer wheel slows down as obstacle gets closer
                outer = int(speed * (0.5 + 0.5 * ratio))

                # Inner wheel slows much more — tighter curve when close
                inner = int(speed * ratio * ratio)

                if left > right:
                    beygja("Vinstri", outer, inner)
                else:
                    beygja("Hægri", outer, inner)

            else:
                turn_dir = "Vinstri" if left > right else "Hægri"
                print(f"Too close! Spinning {turn_dir}...")
                while get_distance(300, 60) <= stop_distance:
                    beygja(turn_dir, speed, 0)
                    time.sleep(0.1)

            time.sleep(0.1)

    finally:
        stop_lidar()