import math
from typing import TypedDict
from pygame import math as gm
from pygame import typing as tp


class Vector2D(gm.Vector2):
    def __floordiv__(self, other): # type: ignore
        if isinstance(other, gm.Vector2):
            return Vector2D(int(self.x/other.x), int(self.y/other.y))
        if isinstance(other, list|tuple) and len(other) == 2:
            return Vector2D(int(self.x/other[0]), int(self.y/other[1]))
    def __truediv__(self, other): # type: ignore
        if isinstance(other, gm.Vector2):
            return Vector2D(self.x/other.x, self.y/other.y)
        if isinstance(other, list|tuple) and len(other) == 2:
            return Vector2D(self.x/other[0], self.y/other[1])
    
    def __rfloordiv__(self, other):
        if isinstance(other, gm.Vector2):
            return Vector2D(int(other.x/self.x), int(other.y/self.x))
        if isinstance(other, list|tuple) and len(other) == 2:
            return Vector2D(int(other[0]/self.x), int(other[1]/self.y))

    def __rtruediv__(self, other): # type: ignore
        if isinstance(other, gm.Vector2):
            return Vector2D(other.x/self.x)
        if isinstance(other, list|tuple) and len(other) == 2:
            return Vector2D(other[0]/self.x, other[1]/self.y)
    


def genesis_to_float(pixel:int, subpixel: int) -> float:
    return pixel + (subpixel / 255)

def hex_to_degrees(hex_angle:int) -> float:
    return (255 - gm.clamp(hex_angle, 0, 255)) / 255 * 360

def degrees_to_hex(degrees:int) -> int:
    return int((360 - degrees) / 360 * 255)

def snap(number, target, range):
    return target*round(number/target) % range

def sin(hex_angle:int) -> int:
    return math.floor(math.sin(hex_to_degrees(hex_angle)))

def cos(hex_angle:int) -> int:
    assert hex_angle in range(0,256), "hex_angle is out of bounds!"
    return math.floor(math.cos(hex_to_degrees(hex_angle)))
