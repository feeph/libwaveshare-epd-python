#!/usr/bin/env python3
"""
abstraction for a framebuffer and it's underlying bytearray
"""

from enum import Enum

# CircuitPython does not provide type hints for these libraries
import adafruit_framebuf  # type: ignore
import PIL.Image


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class FramebufferFormat(Enum):
    GS2_HMSB = adafruit_framebuf.GS2_HMSB  # 2-bit color displays
    GS4_HMSB = adafruit_framebuf.GS4_HMSB  # Unimplemented!
    MHMSB = adafruit_framebuf.MHMSB        # Single bit displays
    MVLSB = adafruit_framebuf.MVLSB        # Single bit displays
    RGB565 = adafruit_framebuf.RGB565      # 16-bit color displays
    RGB888 = adafruit_framebuf.RGB888      # 24-bit color displays


class Rotation(Enum):
    ROTATE_BY_0 = 0    # rotate 0° clockwise
    ROTATE_BY_90 = 1   # rotate 90° clockwise
    ROTATE_BY_180 = 2  # rotate 180° clockwise
    ROTATE_BY_270 = 3  # rotate 270° clockwise


class GenericCanvas:

    def __init__(self, width: int, height: int, fb_length: int, fb_format: FramebufferFormat, fb_rotation: Rotation):
        # initialize frame buffer
        self.buf = bytearray(fb_length)
        self.fb = adafruit_framebuf.FrameBuffer(width=width, height=height, buf=self.buf, buf_format=fb_format)
        self.fb.rotation = fb_rotation.value

    # default implementation - override as needed
    def _is_valid_color(self, color: int) -> bool:
        # accept all 24-bit colors as valid
        return 0 <= color <= 16777216

    # default implementation - override as needed
    def _is_valid_image(self, image: PIL.Image.Image) -> bool:
        # image must have the same width, height and color depth
        if (self.fb.width, self.fb.height) != image.size:
            return False
        else:
            return True

    def get_rotation(self) -> Rotation:
        """
        Get the current rotation setting.
        """
        return Rotation(self.fb.rotation)

    def set_rotation(self, rotation: Rotation):
        """
        Set the rotation (clockwise in 90° steps).
        """
        self.fb.rotation = rotation.value

    def clear(self) -> bool:
        """
        Clear the entire framebuffer.
        (fill with white)
        """
        return self.fill(0xFF)

    def fill(self, color: int) -> bool:
        """
        Fill the entire FrameBuffer with the specified color.
        """
        if self._is_valid_color(color):
            self.fb.fill(color)
            return True
        else:
            return False

    def fill_rect(self, start: Point, width: int, height: int, color: int) -> bool:
        """
        Draw a rectangle at the given location, size and color.
        The ``fill_rect`` method draws both the outline and interior.
        """
        if self._is_valid_color(color):
            self.fb.rect(start.x, start.y, width, height, color, fill=True)
            return True
        else:
            return False

    def get_pixel_color(self, pos: Point) -> int:
        """
        Get the color value of the pixel at this position.
        """
        return self.fb.pixel(pos.x, pos.y)

    def draw_pixel(self, pos: Point, color: int):
        """
        Set the pixel at this position to the given color.
        """
        self.fb.pixel(pos.x, pos.y, color)

    def draw_hline(self, start: Point, width: int, color: int) -> bool:
        """
        Draw a horizontal line up to a given length.
        """
        if self._is_valid_color(color):
            self.fb.hline(start.x, start.y, width, color)
            return True
        else:
            return False

    def draw_vline(self, start: Point, height: int, color: int) -> bool:
        """
        Draw a vertical line up to a given length.
        """
        if self._is_valid_color(color):
            self.fb.vline(start.x, start.y, height, color)
            return True
        else:
            return False

    def draw_circle(self, center: Point, radius: int, color: int) -> bool:
        """
        Draw a circle at the given midpoint location, radius and color.
        The ```circle``` method draws only a 1 pixel outline.
        """
        if self._is_valid_color(color):
            self.fb.circle(center.x, center.y, radius, color)
            return True
        else:
            return False

    def draw_rectangle(self, start: Point, width: int, height: int, color: int, *, fill: bool = False):
        """
        Draw a rectangle at the given location, size and color.
        The ```rect``` method draws only a 1 pixel outline.
        """
        if self._is_valid_color(color):
            self.fb.rect(start.x, start.y, width, height, color, fill)
            return True
        else:
            return False

    def draw_line(self, start: Point, end: Point, color: int) -> bool:
        # pylint: disable=too-many-arguments
        """
        draw a line between the specified coordinates
        """
        if self._is_valid_color(color):
            self.fb.line(start.x, start.y, end.x, end.y, color)
            return True
        else:
            return False

    def scroll_canvas(self, delta_x: int, delta_y: int):
        """
        shifts framebuf in x and y direction
        """
        self.fb.scroll(delta_x, delta_y)

    # pylint: disable=too-many-arguments
    def draw_text(self, string: str, pos: Point, color: int, *, font_name: str = "font5x8.bin", size: int = 1) -> bool:
        r"""
        Place text on the screen in variables sizes.
        Multi-line text can be provided using '\n' to indicate newlines.

        Does not word-wrap if text goes off screen.
        """
        if self._is_valid_color(color):
            self.fb.text(string, pos.x, pos.y, color, font_name=font_name, size=size)
            return True
        else:
            return False

    def draw_image(self, img: PIL.Image.Image) -> bool:
        """
        Set buffer to value of Python Imaging Library image.

        The image must conform to the width and height of this canvas and
        have the correct color depth.
        """
        if self._is_valid_image(img):
            self.fb.image(img)
            return True
        else:
            return False
