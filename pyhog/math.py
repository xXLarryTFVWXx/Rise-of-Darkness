from dataclasses import dataclass
from ctypes import c_uint8, c_uint16, c_int8, c_int16
from typing import List, Tuple


class uint8(c_uint8):
    def __add__(self, other):
        if isinstance(other, int):
            return uint8(self.value + other)
        if isinstance(other, uint8):
            return uint8(self.value + other.value)
        raise TypeError("Can't add {} to {}".format(type(other), type(self)))
    def __sub__(self, other):
        if isinstance(other, int):
            return uint8(self.value - other)
        if isinstance(other, uint8):
            return uint8(self.value - other.value)
        raise TypeError("Can't subtract {} from {}".format(type(other), type(self)))
    def __mul__(self, other):
        if isinstance(other, int):
            return uint8(self.value * other)
        if isinstance(other, uint8):
            return uint8(self.value * other.value)
        raise TypeError("Can't multiply {} by {}".format(type(other), type(self)))
    def __truediv__(self, other):
        if isinstance(other, int):
            return uint8(self.value / other)
        if isinstance(other, uint8):
            return uint8(self.value / other.value)
        raise TypeError("Can't divide {} by {}".format(type(other), type(self)))
    def __floordiv__(self, other):
        if isinstance(other, int):
            return uint8(self.value // other)
        if isinstance(other, uint8):
            return uint8(self.value // other.value)
        raise TypeError("Can't divide {} by {}".format(type(other), type(self)))
    def __mod__(self, other):
        if isinstance(other, int):
            return uint8(self.value % other)
        if isinstance(other, uint8):
            return uint8(self.value % other.value)
        raise TypeError("Can't mod {} by {}".format(type(other), type(self)))
    def __pow__(self, other):
        if isinstance(other, int):
            return uint8(self.value ** other)
        if isinstance(other, uint8):
            return uint8(self.value ** other.value)
        raise TypeError("Can't power {} by {}".format(type(other), type(self)))
    def __repr__(self):
        return f"uint8({self.value})"
    def __str__(self):
        return f"{self.value}"
@dataclass
class Vector2:
    def __init__(self, x, y, angle=0, retro_mode=False):
        """Right now retro_mode is not implemented
            once it is, it will be used to better emulate
            the angles used for the Sonic the Hedgehog games on the Sega Genesis/Mega Drive
        """
        self.x = x
        self.y = y
        self.angle = uint8(angle)
        self.retro_mode = retro_mode
    def rotate(self, angle) -> None:
        if isinstance(angle, int):
            self.angle += angle if self.retro_mode else -(angle%256)
            return None
        raise TypeError("angle must be an int")
    