#!/usr/bin/env python3

import PIL
from overrides import override

from .generic import FramebufferFormat, GenericCanvas, Rotation


class MonochromeCanvas(GenericCanvas):

    def __init__(self, width: int, height: int, fb_rotation: Rotation):
        fb_length = height * width // 8  # 1 bit per pixel
        fb_format = FramebufferFormat.MHMSB
        super().__init__(width=width, height=height, fb_length=fb_length, fb_format=fb_format, fb_rotation=fb_rotation)

    @override
    def _is_valid_color(self, color):
        # only valid colors are
        #   0x00 (black)
        #   0xff (white)
        return color in [0x00, 0xFF]

    @override
    def _is_valid_image(self, image: PIL.Image) -> bool:
        # image must have the same width, height and color depth
        if image.size != (self.fb.width, self.fb.height):
            # image has different dimensions
            return False
        elif image.mode != 'L':
            # image is not grayscale ('luminance')
            return False
        else:
            return True
