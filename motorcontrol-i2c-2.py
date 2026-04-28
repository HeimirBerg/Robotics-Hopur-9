import smbus
import time

I2C_ADDRESS = 0x50   # Arduino slave address
bus = smbus.SMBus(1) # I2C bus on Pi Zero / Pi 3 / Pi 4

print("I2C motor controller ready.")
print("Enter speeds as: motor1, motor2  (range -255 to 255)\n")

while True:
    try:
        value = input("Enter speeds: ").strip()

        # Split input
        parts = value.split(",")
        if len(parts) != 2:
            print("Format error. Use: 50, -100")
            continue

        # Convert to integers
        m1 = int(parts[0].strip())
        m2 = int(parts[1].strip())

        # Validate range
        if not (-255 <= m1 <= 255 and -255 <= m2 <= 255):
            print("Each value must be between -255 and 255.")
            continue

        # Split into magnitude + sign
        m1_speed = abs(m1)
        m1_sign  = 0 if m1 >= 0 else 1

        m2_speed = abs(m2)
        m2_sign  = 0 if m2 >= 0 else 1

        # Pack into 4 bytes: [speed1, sign1, speed2, sign2]
        data = [m1_speed, m1_sign, m2_speed, m2_sign]

        # Send via I2C
        bus.write_i2c_block_data(I2C_ADDRESS, 0x00, data)

        print(f"Sent speeds → Motor1: {m1}, Motor2: {m2}")

    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except ValueError:
        print("Invalid number format.")
    except Exception as e:
        print("I2C Error:", e)
        time.sleep(0.5)
