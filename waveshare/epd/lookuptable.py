#!/usr/bin/env python3

class LookupTable:

    def __init__(self, lut: bytearray, unk1: int, gate: int, src: bytearray, vcom: int):
        if isinstance(lut, bytearray) and len(lut) == 153:
            self.lut = lut
        else:
            raise ValueError('lookup table must contain 153 entries')
        self.unk1 = unk1
        self.gate = gate
        if isinstance(src, bytearray) and len(src) == 3:
            self.src = src
        else:
            raise ValueError('source voltage must contain 3 entries')
        self.vcom = vcom
