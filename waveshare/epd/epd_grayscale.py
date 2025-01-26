#!/usr/bin/env python3

import busio
import digitalio

import waveshare.canvas

from .epd_generic import EPD_generic
from .lookuptable import LookupTable


# colors            0x24    0x26
# 0b1111_1111  -> 0b1111  0b1111
# 0b1010_1010  -> 0b1111  0b0000
# 0b0101_0101  -> 0b0000  0b1111
# 0b0000_0000  -> 0b0000  0b0000
def split_framebuffer(buf: bytearray) -> tuple[bytearray, bytearray]:
    # the smallest available display has a resolution of 200x200 and is
    # black and white. This means the smallest buffer size is 5kB.
    fb_len = len(buf)  # 5000 <= x <= 240_000
    if fb_len % 2 != 0:
        # theoretically it would be possible to create a display with
        # 4 grayscale pixels (1 byte) but no such device exists
        raise ValueError("buffer length must be divisible by 2!")

    # we can pre-allocate the buffers since we know the final size
    # (this avoids dynamic reallocation)
    buf_24 = bytearray(int(fb_len/2))
    buf_26 = bytearray(int(fb_len/2))

    # To get started in a known-good state we're going to test each bit
    # individually and set the output buffer accordingly. There may be
    # better approaches but this naive approach should help to get the
    # unit tests set up and validated.
    for i in range(0, fb_len, 2):
        byte_24 = 0x00
        byte_26 = 0x00

        if buf[i] & 0b1000_0000:
            byte_24 += 0b1000_0000
        if buf[i] & 0b0010_0000:
            byte_24 += 0b0100_0000
        if buf[i] & 0b0000_1000:
            byte_24 += 0b0010_0000
        if buf[i] & 0b0000_0010:
            byte_24 += 0b0001_0000
        if buf[i+1] & 0b1000_0000:
            byte_24 += 0b0000_1000
        if buf[i+1] & 0b0010_0000:
            byte_24 += 0b0000_0100
        if buf[i+1] & 0b0000_1000:
            byte_24 += 0b0000_0010
        if buf[i+1] & 0b0000_0010:
            byte_24 += 0b0000_0001

        if buf[i] & 0b0100_0000:
            byte_26 += 0b1000_0000
        if buf[i] & 0b0001_0000:
            byte_26 += 0b0100_0000
        if buf[i] & 0b0000_0100:
            byte_26 += 0b0010_0000
        if buf[i] & 0b0000_0001:
            byte_26 += 0b0001_0000
        if buf[i+1] & 0b0100_0000:
            byte_26 += 0b0000_1000
        if buf[i+1] & 0b0001_0000:
            byte_26 += 0b0000_0100
        if buf[i+1] & 0b0000_0100:
            byte_26 += 0b0000_0010
        if buf[i+1] & 0b0000_0001:
            byte_26 += 0b0000_0001
        buf_24[int(i/2)] = byte_24
        buf_26[int(i/2)] = byte_26

    return (buf_24, buf_26)


Gray4 = LookupTable(
    lut = bytearray([
        0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x20, 0x60, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x28, 0x60, 0x14, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2A, 0x60, 0x15, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x90,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x02, 0x00, 0x05, 0x14, 0x00, 0x00, 0x1E, 0x1E, 0x00,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x05, 0x14, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x24, 0x22, 0x22, 0x22, 0x23, 0x32,
        0x00, 0x00,	0x00
    ]),
    unk1 = 0x22,
    gate = 0x17,
    src  = bytearray([0x41, 0xAE, 0x32]),
    vcom = 0x28,
)


class EPD_grayscale(EPD_generic):

    def __init__(self, spi_bus: busio.SPI, bsy: digitalio.DigitalInOut, dcs: digitalio.DigitalInOut, rst: digitalio.DigitalInOut, scs: digitalio.DigitalInOut):
        super().__init__(spi_bus=spi_bus, bsy=bsy, dcs=dcs, rst=rst, scs=scs)
        print("hardware init (grayscale)")
        self.reset()
        self.read_busy()
        self.send_command(0x12)  # SWRESET
        self.read_busy() 
        self.send_command(0x01, bytearray([0x27, 0x01, 0x00]))  # driver output control      
        self.send_command(0x11, 0x03)  # data entry mode       
        self.set_window(8, 0, self.width, self.height-1)
        self.send_command(0x3C, 0x04)
        self.set_cursor(1, 0)
        self.read_busy()
        self.set_lut(Gray4)
        # # initialize frame buffer
        # self.buf = bytearray(height * width // 4)
        # self.fb = adafruit_framebuf.FrameBuffer(self.buf, width=width, height=height, buf_format=adafruit_framebuf.GS2_HMSB)  # framebuf.GS2_HMSB
        # define available colors
        # self.black = 0x00
        # self.white = 0xff
        # self.darkgray = 0xaa
        # self.grayish = 0x55

    def display(self, canvas: waveshare.canvas.GenericCanvas):
        len1 = len(canvas.buf)
        buf1 = bytearray(len1)
        for i in range(len1):
            temp3=0
            for j in range(0, 2):
                temp1 = canvas.buf[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x00   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x01   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x00
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x01
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    
                    if (( j!=1 ) | ( k!=1 )):
                        temp3 <<= 1
                    temp1 >>= 2
            buf1[i] = temp3
        self.send_command(0x24, buf1)
            
        len2 = len(canvas.buf)
        buf2 = bytearray(len2)
        for i in range(len2):
            temp3=0
            for j in range(0, 2):
                temp1 = canvas.buf[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x00   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x01   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x00
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x01
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2  
                    if(j!=1 or k!=1):                    
                        temp3 <<= 1
                    temp1 >>= 2
            buf2[i] = temp3
        self.send_command(0x26, buf2)

        self.turn_on_display()
