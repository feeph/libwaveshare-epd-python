#!/usr/bin/env python3

from .epd_monochrome import EPD_monochrome
from .epd_grayscale import EPD_grayscale

# colors

# monochrome mode (1 byte = 8 pixels)
#   black:      0b0
#   white:      0b1

# grayscale mode (1 byte = 4 pixels)
#   black:      0b00
#   dark gray:  0b10
#   light gray: 0b01
#   white:      0bff

# black/white/red (1 byte = 4 pixels)
#   black:      0b00
#   red:        0b01
#   white:      0bff

# The display divides a four-grayscale picture into two pictures. The
# pixels in the same position of pictures are combined into one pixel.
# There are 4 combinations of this point, that is, 4 gray levels:

# monochrome mode:
#  -> send framebuffer to 0x24
# grayscale mode:
#                            framebuffer: 00 10 01 11
#  -> send 1st bit of each pixel to 0x24: 0  1  0  1   0x24 = 0b0101
#  -> send 2nd bit of each pixel to 0x26:  0  0  1  1  0x26 = 0b0011

# permanent damage

# Note that the screen cannot be powered on for a long time. When the screen is not refreshed, please set the screen to sleep mode, or power off the e-Paper. Otherwise, the screen will remain in a high voltage state for a long time, which will damage the e-Paper and cannot be repaired!