# ---------- Motor Control ---------- #
# Þessi kóði hefur samskipti við Motor Control Unitið (MCU) og sendir á það skipanir.
# Auk þess eru föll sem lagfæra formerki á hraða til að geta sent rétt á MCU.

import src.addresses as a
import smbus as s

# Setup
I2C_ADDRESS = a.MCU         # Slave addres
DATA_ADDRESS = a.MCU_WRITE  # Pi address to write data
bus = s.SMBus(1)            # I2C bus on Pi 4


def send_speeds(m1: int, m2: int) -> str:
    """Sends speeds in range [-255, 255] to motors 1 and 2 (m1 and m2) via the Motor Control Unit."""
    try:
        # Check if integers
        m1 = int(m1)
        m2 = int(m2)

        # Validate range.
        if not ((-255 <= m1 <= 255) and (-255 <= m2 <= 255)):
            return f"Requested speeds {m1} or {m2} are out of range [-255, 255]."

        # Split into magnitude + sign
        m1_speed = abs(m1)
        m1_sign = 0 if m1 >= 0 else 1

        m2_speed = abs(m2)
        m2_sign = 1 if m2 >= 0 else 0 # Inverted sign to correct direction of rotation

        # Actual m2 value sent to MCU
        m2 = -m2 if m2_sign == 1 else m2

        # Pack data into 4 bytes [speed1, sign1, speed2, sign2]
        data = [m1_speed, m1_sign, m2_speed, m2_sign]

        # Send to MCU via I2C
        bus.write_i2c_block_data(I2C_ADDRESS, DATA_ADDRESS, data)

    except ValueError:
        return "Invalid number format"
    
    return f"Speeds sent, Motor 1: {m1}, Motor 2: {m2}."


def forward(speed: int) -> str:
    """Converts a single speed input so it can be sent to the motors with correct signs."""
    try:
        m = int(speed)
        send_speeds(m,m)

    except ValueError:
        return "Invalid number format"

    return f"Speed {speed} sent as {m}."
    

def reverse(speed: int) -> str:
    """Converts a single speed input so it can be sent to the motors with correct signs."""
    try:
        m = int(speed)
        send_speeds(-m,-m)

    except ValueError:
        return "Invalid number format"
    
    return f"Speed {speed} sent as {m}."

    
def turn_left(speed: int, ratio=255.0) -> str:
    """Sends speeds to turn left in different ratios."""
    try:
        velocity = int(speed)

        # Calculate motor values
        m1 = (velocity/ratio)
        m2 = velocity
        m1 = int(m1)

        print(send_speeds(m1,m2))

    except ValueError:
        return "Invalid number format."
    
    return f"Speed {speed} at ratio {ratio} sent as {m1}, {m2}."


def turn_right(speed: int, ratio=255.0) -> str:
    """Sends speeds to turn right in different ratios."""
    try:
        velocity = int(speed)

        # Calculate motor values
        m1 = velocity
        m2 = (velocity/ratio)
        m2 = int(m2)

        print(send_speeds(m1,m2))

    except ValueError:
        return "Invalid number format."
    
    return f"Speed {speed} at ratio {ratio} sent as {m1}, {m2}."


def stop() -> str:
    send_speeds(0,0)
    return "Stopped motors"
