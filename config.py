from typing import Any, Self

# ------------------------------
#      Fastar
# ------------------------------

MIN_VELOCITY = -255
MAX_VELOCITY =  255

MIN_SPEED    =   15
MAX_SPEED    =  255

MIN_TURN     =   -1
MAX_TURN     =    3


# ------------------------------
#      Addressur
# ------------------------------

# Motor Control Unit
MCU       = 0x50  # I2C Addressa
MCU_WRITE = 0x00  # Data register á Pi



# ------------------------------
#      Value Klassar
# ------------------------------

class Speed(int):
    def __new__(cls, value: Any) -> Self:
        val = int(value)
        if not MIN_SPEED <= val <= MAX_SPEED:
            raise ValueError("Stærð hraða þarf að vera á bilinu [15 til 255].")
        return super().__new__(cls, val)
    
class Velocity(int):
    def __new__(cls, value: Any) -> Self:
        val = int(value)
        if not MIN_VELOCITY <= val <= MAX_VELOCITY:
            raise ValueError("Átt og stærð hraða þarf að vera á bilinu [-255 til 255].")
        return super().__new__(cls, val)
    
class TurnStage(int):
    def __new__(cls, value: Any) -> Self:
        val = int(value)
        if not (MIN_TURN <= val <= MAX_TURN):
            raise ValueError("Beygju stig a þarf að vera á bilinu [-1 til 3].")
        return super().__new__(cls, val)