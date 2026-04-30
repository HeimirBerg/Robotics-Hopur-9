
# ---------- Motor Control ---------- #
# Þessi kóði hefur samskipti við Motor Control Unitið (MCU) og sendir á það skipanir.
# Auk þess eru föll sem lagfæra formerki á hraða til að geta sent rétt á MCU.

from src import addresses as a

I2C_ADDRESS = a.MCU

b = a.SENSOR_L
g = a.SERVO_L