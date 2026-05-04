import serial

port = "/dev/ttyUSB0"  # change if needed
baud = 115200           # common for DFR1023, may need adjusting

with serial.Serial(port, baud, timeout=1) as ser:
    for _ in range(20):
        line = ser.readline()
        print(line)