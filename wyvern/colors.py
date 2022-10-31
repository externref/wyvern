# MIT License

# Copyright (c) 2022 Sarthak

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

import colorsys
import random
import re
import typing

__all__: tuple[str, ...] = (
    "Color",
    "Colour",
)


@typing.final
class Color:
    """
    Class representing a color in the RGB color space.
    Alias name Colour exists for convenience.

    Attributes
    ----------
    value : int
        The value of the color. This is a 24-bit integer, where the first 8 bits are the red value,
        the next 8 bits are the green value, and the last 8 bits are the blue value.
    """

    __slots__: tuple[str, ...] = ("value",)

    RGB_REGEX: re.Pattern[str] = re.compile(r"rgb\((\d{1,3}), (\d{1,3}), (\d{1,3})\)")
    HSL_REGEX: re.Pattern[str] = re.compile(r"hsl\((\d{1,3}), (\d{1,3})%, (\d{1,3})%\)")
    HSV_REGEX: re.Pattern[str] = re.compile(r"hsv\((\d{1,3}), (\d{1,3})%, (\d{1,3})%\)")
    HEX_REGEX: re.Pattern[str] = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})")

    def __init__(self, value: int) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Color({self.value})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Color) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __ne__(self, other: object) -> bool:
        return self is not other

    @classmethod
    def from_hex(cls, hex_value: str) -> Color:
        """
        Creates a Color object from a hex value.

        Parameters
        ----------

        hex_value: str
            The hex value to use.

        Returns
        -------

        wyvern.Color
            A Color object.

        Examples
        --------

            >>> Color.from_hex('#ff0000')
            Color(16776960)
            >>> Color.from_hex('#00ff00')
            Color(255)
            >>> Color.from_hex('#0000ff')
            Color(0)
        """
        if match := cls.HEX_REGEX.match(hex_value):
            hex_value = match.group(1)
            if len(hex_value) == 3:
                hex_value = "".join(c * 2 for c in hex_value)
            return cls(int(hex_value, 16))
        raise ValueError(f"Invalid hex value: {hex_value}")

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> Color:
        """
        Creates a Color object from RGB values.

        Parameters
        ----------
        r: int
            The red value.
        g: int
            The green value.
        b: int
            The blue value.

        Returns
        -------
        wyvern.Color
            A Color object.

        Examples
        --------

            >>> Color.from_rgb(255, 0, 0)
            Color(16711680)
            >>> Color.from_rgb(0, 255, 0)
            Color(65280)
            >>> Color.from_rgb(0, 0, 255)
            Color(255)
        """
        return cls((r << 16) + (g << 8) + b)

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float) -> Color:
        """
        Creates a Color object from HSV values.

        Parameters
        ----------
        h: float
            The hue value.
        s: float
            The saturation value.
        v: float
            The value in HSV color space.

        Returns
        -------
        wyvern.Color
            A Color object.

        Examples
        --------

            >>> Color.from_hsv(0, 1, 1)
            Color(16711680)
            >>> Color.from_hsv(120, 1, 1)
            Color(16711680)
            >>> Color.from_hsv(240, 1, 1)
            Color(16711680)

        """
        return cls.from_rgb(*[int(round(c * 255)) for c in colorsys.hsv_to_rgb(h, s, v)])

    @classmethod
    def from_hsl(cls, h: float, s: float, l: float) -> Color:
        """
        Creates a Color object from HSL values.

        Parameters
        ----------
        h: float
            The hue value.
        s: float
            The saturation value.
        l: float
            The lightness value.

        Returns
        -------
        wyvern.Color
            A Color object.

        Examples
        --------

            >>> Color.from_hsl(0, 1, 0.5)
            Color(16711680)
            >>> Color.from_hsl(120, 1, 0.5)
            Color(16711680)
            >>> Color.from_hsl(240, 1, 0.5)
            Color(16711680)
        """
        return cls.from_rgb(*[int(round(c * 255)) for c in colorsys.hls_to_rgb(h, l, s)])

    @classmethod
    def from_random(cls) -> Color:
        """
        Creates a Color object from a random color. Randomly generates a color in the RGB color space.

        Returns
        -------

        wyvern.Color
            A Color object.
        """
        return cls.from_rgb(*[random.randint(0, 255) for _ in range(3)])

    @classmethod
    def from_string(cls, string: str) -> Color:
        """
        Creates a Color object from a string.

        Parameters
        ----------

        string: str
            The string to use.

        Returns
        -------

        wyvern.Color
            A Color object.

        Examples
        --------

            >>> Color.from_string('rgb(255, 0, 0)')
            Color(16711680)
            >>> Color.from_string('hsl(0, 100%, 50%)')
            Color(-80727249750)
            >>> Color.from_string('hsv(0, 100%, 100%)')
            Color(1022371500)
            >>> Color.from_string('#ff0000')
            Color(16776960)

        """
        if string.startswith("#"):
            return cls.from_hex(string)
        elif match := cls.RGB_REGEX.match(string):
            return cls.from_rgb(*[int(c) for c in match.groups()])
        elif match := cls.HSL_REGEX.match(string):
            return cls.from_hsl(*[float(c) for c in match.groups()])
        elif match := cls.HSV_REGEX.match(string):
            return cls.from_hsv(*[float(c) for c in match.groups()])
        raise ValueError(f"Invalid color string: {string}")

    @classmethod
    def default(cls) -> Color:
        """
        Creates a Color object from the default color. This is `0x000000`. (Black)

        Examples
        --------

            >>> Color.default()
            Color(0)

        """
        return cls(0x000000)

    @property
    def hex(self) -> str:
        """The hex value of the color."""
        return f"#{self.value:06x}"

    @property
    def rgb(self) -> tuple[int, int, int]:
        """The RGB values of the color."""
        return (self.value >> 16) & 0xFF, (self.value >> 8) & 0xFF, self.value & 0xFF

    @property
    def hsv(self) -> tuple[float, float, float]:
        """The HSV values of the color."""
        return colorsys.rgb_to_hsv(*(c / 255 for c in self.rgb))

    @property
    def hsl(self) -> tuple[float, float, float]:
        """The HSL values of the color."""
        return colorsys.rgb_to_hls(*(c / 255 for c in self.rgb))

    @property
    def r(self) -> int:
        """The red value of the color."""
        return self.rgb[0]

    @property
    def g(self) -> int:
        """The green value of the color."""
        return self.rgb[1]

    @property
    def b(self) -> int:
        """The blue value of the color."""
        return self.rgb[2]

    @classmethod
    def red(cls) -> Color:
        """Creates a Color object from the red color. This is `0xff0000`. (Red)"""
        return cls(0xFF0000)

    @classmethod
    def green(cls) -> Color:
        """Creates a Color object from the green color. This is `0x00ff00`. (Green)"""
        return cls(0x00FF00)

    @classmethod
    def blue(cls) -> Color:
        """Creates a Color object from the blue color. This is `0x0000ff`. (Blue)"""
        return cls(0x0000FF)

    @classmethod
    def yellow(cls) -> Color:
        """Creates a Color object from the yellow color. This is `0xffff00`. (Yellow)"""
        return cls(0xFFFF00)

    @classmethod
    def cyan(cls) -> Color:
        """Creates a Color object from the cyan color. This is `0x00ffff`. (Cyan)"""
        return cls(0x00FFFF)

    @classmethod
    def magenta(cls) -> Color:
        """Creates a Color object from the magenta color. This is `0xff00ff`. (Magenta)"""
        return cls(0xFF00FF)

    @classmethod
    def black(cls) -> Color:
        """Creates a Color object from the black color. This is `0x000000`. (Black)"""
        return cls(0x000000)

    @classmethod
    def white(cls) -> Color:
        """Creates a Color object from the white color. This is `0xffffff`. (White)"""
        return cls(0xFFFFFF)

    @classmethod
    def gray(cls) -> Color:
        """Creates a Color object from the gray color. This is `0x808080`. (Gray)"""
        return cls(0x808080)

    @classmethod
    def grey(cls) -> Color:
        """Creates a Color object from the grey color. This is `0x808080`. (Grey)"""
        return cls(0x808080)

    @classmethod
    def orange(cls) -> Color:
        """Creates a Color object from the orange color. This is `0xffa500`. (Orange)"""
        return cls(0xFFA500)


Colour = Color
