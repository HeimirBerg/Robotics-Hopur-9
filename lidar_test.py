#!/usr/bin/env python3
"""
RPLiDAR S2L diagnostic script — raw pyserial, no pyrplidar dependency.
Tested against: RPLiDAR S2L (model 113), /dev/ttyUSB0, 1 000 000 baud.

Usage:
    python3 lidar_test.py
"""

import serial
import time
import struct
import sys

PORT = '/dev/ttyUSB0'
BAUD = 1_000_000

# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def checksum(payload: bytes) -> int:
    c = 0
    for b in payload:
        c ^= b
    return c & 0x7F


def send_cmd(s: serial.Serial, cmd: int, payload: bytes = b'') -> None:
    pkt = bytes([0xA5, cmd])
    if payload:
        pkt += bytes([len(payload)]) + payload + bytes([checksum(payload)])
    s.write(pkt)
    s.flush()


def read_descriptor(s: serial.Serial):
    """Read the 7-byte response descriptor. Returns (data_len, data_type)."""
    raw = s.read(7)
    if len(raw) < 7:
        print(f"  [timeout — got only {len(raw)} bytes: {raw.hex()}]")
        return None, None
    if raw[0] != 0xA5 or raw[1] != 0x5A:
        print(f"  [bad sync bytes: {raw.hex()}]")
        return None, None
    dlen = struct.unpack('<I', raw[2:6])[0] & 0x3FFFFFFF
    dtype = raw[6]
    return dlen, dtype


# ---------------------------------------------------------------------------
# Main diagnostic sequence
# ---------------------------------------------------------------------------

def main():
    print(f"Opening {PORT} at {BAUD} baud...")
    try:
        s = serial.Serial(PORT, BAUD, timeout=3)
    except serial.SerialException as e:
        sys.exit(f"ERROR: {e}")

    # ------------------------------------------------------------------
    # 1. RESET (0x40) — clears any latched motor protection fault
    # ------------------------------------------------------------------
    print("\n[1] RESET (0xA5 0x40)")
    send_cmd(s, 0x40)
    time.sleep(2.5)
    banner = s.read(s.in_waiting or 64)
    print(f"    boot banner ({len(banner)} bytes): {banner[:60]!r}")
    s.reset_input_buffer()

    # ------------------------------------------------------------------
    # 2. GET_INFO (0x50)
    # ------------------------------------------------------------------
    print("\n[2] GET_INFO (0xA5 0x50)")
    send_cmd(s, 0x50)
    dlen, dtype = read_descriptor(s)
    if dlen:
        d = s.read(dlen)
        print(f"    model={d[0]}, fw={d[2]}.{d[1]}, hw={d[3]}")
        print(f"    serial={d[4:].hex().upper()}")
    else:
        print("    no response to GET_INFO")

    # ------------------------------------------------------------------
    # 3. GET_HEALTH (0x52)
    # ------------------------------------------------------------------
    print("\n[3] GET_HEALTH (0xA5 0x52)")
    send_cmd(s, 0x52)
    dlen, dtype = read_descriptor(s)
    if dlen:
        d = s.read(dlen)
        status = d[0]
        errcode = struct.unpack('<H', d[1:3])[0]
        labels = {0: 'GOOD', 1: 'WARNING', 2: 'ERROR'}
        print(f"    status={status} ({labels.get(status, '?')}), "
              f"error_code={errcode} ({errcode:#06x})")
        if errcode == 0x400:
            print("    *** 0x400 = motor protection latch — motor not spinning ***")
    else:
        print("    no response to GET_HEALTH")

    # ------------------------------------------------------------------
    # 4. EXPRESS_SCAN submode 4 — Ultra Capsule (correct mode for S2/S2L)
    # ------------------------------------------------------------------
    print("\n[4] EXPRESS_SCAN (0xA5 0x82) submode=4 (Ultra Capsule)")
    send_cmd(s, 0x82, bytes([4, 0, 0, 0, 0]))
    dlen, dtype = read_descriptor(s)
    print(f"    descriptor: dlen={dlen}, dtype={hex(dtype) if dtype is not None else 'N/A'}")
    if dlen and dlen > 0:
        print("    Motor appears to be running — reading 10 capsule packets:")
        for i in range(10):
            pkt = s.read(dlen)
            if pkt:
                print(f"    [{i:02d}] {pkt.hex()}")
            else:
                print(f"    [{i:02d}] timeout")
    else:
        print("    No data stream — motor likely still not spinning")

    # ------------------------------------------------------------------
    # 5. Fallback: reset again, then try EXPRESS_SCAN submode 2 (Dense)
    # ------------------------------------------------------------------
    print("\n[5] RESET then EXPRESS_SCAN submode=2 (Dense Boost, fallback)")
    s.reset_input_buffer()
    send_cmd(s, 0x40)
    time.sleep(2.5)
    s.reset_input_buffer()
    send_cmd(s, 0x82, bytes([2, 0, 0, 0, 0]))
    dlen, dtype = read_descriptor(s)
    print(f"    descriptor: dlen={dlen}, dtype={hex(dtype) if dtype is not None else 'N/A'}")
    if dlen and dlen > 0:
        print("    Reading 5 packets:")
        for i in range(5):
            pkt = s.read(dlen)
            print(f"    [{i:02d}] {pkt.hex() if pkt else 'timeout'}")
    else:
        print("    No data stream on submode 2 either")

    # ------------------------------------------------------------------
    # 6. GET_HEALTH again — check if latch cleared after scan attempt
    # ------------------------------------------------------------------
    print("\n[6] GET_HEALTH again (post-scan)")
    s.reset_input_buffer()
    send_cmd(s, 0x52)
    dlen, dtype = read_descriptor(s)
    if dlen:
        d = s.read(dlen)
        status = d[0]
        errcode = struct.unpack('<H', d[1:3])[0]
        labels = {0: 'GOOD', 1: 'WARNING', 2: 'ERROR'}
        print(f"    status={status} ({labels.get(status, '?')}), "
              f"error_code={errcode} ({errcode:#06x})")
    else:
        print("    no response")

    s.close()
    print("\nDone.")


if __name__ == '__main__':
    main()