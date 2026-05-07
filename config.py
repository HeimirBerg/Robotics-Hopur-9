from typing import Any, Self

class Speed(int):
    def __new__(cls, value: Any) -> Self:
        val = int(value)
        if not 15 <= val <= 255:
            raise ValueError("Stærð hraða þarf að vera á bilinu [15 til 255].")
        return super().__new__(cls, val)
    
class Velocity(int):
    def __new__(cls, value: Any) -> Self:
        val = int(value)
        if not -255 <= val <= 255:
            raise ValueError("Átt og stærð hraða þarf að vera á bilinu [-255 til 255].")
        return super().__new__(cls, val)
    
class TurnStage(int):
    def __new__(cls, value: Any) -> Self:
        val = int(value)
        if not (-1 <= val <= 3):
            raise ValueError("Beygju stig a þarf að vera á bilinu [-1 til 3].")
        return super().__new__(cls, val)