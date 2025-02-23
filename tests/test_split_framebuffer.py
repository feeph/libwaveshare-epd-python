#!/usr/bin/env python3
"""
verify the framebuffer is split correctly
"""
# pylint: disable=missing-class-docstring,missing-function-docstring

import unittest

from waveshare.epd.epd_grayscale import split_framebuffer


class TestFrameBuffer(unittest.TestCase):

    # ---------------------------------------------------------------------
    # test if the colors are split properly
    # ---------------------------------------------------------------------

    def test_all_black(self):
        buffer = bytearray([0b1111_1111, 0b1111_1111]) # 8 black pixels (8 x 0b11)
        # -----------------------------------------------------------------
        computed = split_framebuffer(buffer)
        expected = (bytearray([0b1111_1111]), bytearray([0b1111_1111]))
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_all_dark(self):
        buffer = bytearray([0b1010_1010, 0b1010_1010]) # 8 dark grey pixels (8 x 0b10)
        # -----------------------------------------------------------------
        computed = split_framebuffer(buffer)
        expected = (bytearray([0b1111_1111]), bytearray([0b0000_0000]))
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_all_light(self):
        buffer = bytearray([0b0101_0101, 0b0101_0101]) # 8 light grey pixels (8x 0b01)
        # -----------------------------------------------------------------
        computed = split_framebuffer(buffer)
        expected = (bytearray([0b0000_0000]), bytearray([0b1111_1111]))
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_all_white(self):
        buffer = bytearray([0b0000_0000, 0b0000_0000]) # 8 white pixels (8 x 0b00)
        # -----------------------------------------------------------------
        computed = split_framebuffer(buffer)
        expected = (bytearray([0b0000_0000]), bytearray([0b0000_0000]))
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    # ---------------------------------------------------------------------
    # test if the order of bits is preserved properly
    # ---------------------------------------------------------------------

    def test_mixed(self):
        buffer = bytearray([0b1110_0100, 0b1110_0100]) # black, dark grey, light grey, white; repeat
        # -----------------------------------------------------------------
        computed = split_framebuffer(buffer)
        expected = (bytearray([0b1100_1100]), bytearray([0b1010_1010]))
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)

    def test_pixel_order(self):
        buffer = bytearray([0b1010_1010, 0b0101_0101]) # dark, dark, dark, dark, light, light, light, light
        # -----------------------------------------------------------------
        computed = split_framebuffer(buffer)
        expected = (bytearray([0b1111_0000]), bytearray([0b0000_1111]))
        # -----------------------------------------------------------------
        self.assertEqual(computed, expected)


if __name__ == '__main__':
    unittest.main()
