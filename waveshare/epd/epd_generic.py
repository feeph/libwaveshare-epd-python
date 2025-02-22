#!/usr/bin/env python3

import time

import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice

import waveshare.canvas
from waveshare.epd.lookuptable import LookupTable

WF_PARTIAL_2IN9 = LookupTable(
    lut=bytearray([
        0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x40, 0x40, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,
        0x00, 0x00, 0x00
    ]),
    unk1=0x22,
    gate=0x17,
    src=bytearray([0x41, 0xB0, 0x32]),
    vcom=0x36,
)


class EPD_generic:
    """
    base class for ePaper Display
    """

    def __init__(self, spi_bus: busio.SPI, bsy: digitalio.DigitalInOut, dcs: digitalio.DigitalInOut, rst: digitalio.DigitalInOut, scs: digitalio.DigitalInOut):  # noqa: E501
        self.busy_pin = bsy
        self.cs_pin = scs
        self.dc_pin = dcs
        self.reset_pin = rst
        self.spi_bus = spi_bus
        self.spi_baudrate = 4_000_000

    def _display(self, canvas1: waveshare.canvas.GenericCanvas, canvas2: waveshare.canvas.GenericCanvas | None = None):
        # it is unclear what the difference between buf1 and buf2 is
        # (in the provided examples buf1 and buf2 are always set to the same value)
        self.send_command(0x24, canvas1.buf)  # WRITE_RAM
        if canvas2 is not None:
            self.send_command(0x26, canvas2.buf)  # WRITE_RAM
        self.turn_on_display()

    def _display_partial(self, canvas: waveshare.canvas.GenericCanvas):
        self.reset_pin.value = 0
        time.sleep(0.002)
        self.reset_pin.value = 1
        time.sleep(0.002)
        self.set_lut(WF_PARTIAL_2IN9)
        self.send_command(0x37, bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00]))
        self.send_command(0x3C, 0x80)  # BorderWaveform
        self.send_command(0x22, 0xC0)
        self.send_command(0x20)
        self.read_busy()
        self.set_window(0, 0, canvas.fb.width - 1, canvas.fb.height - 1)
        self.set_cursor(0, 0)
        self.send_command(0x24, canvas.buf)  # WRITE_RAM
        self.turn_on_display_partial()

    def reset(self):
        """
        hardware reset
        """
        print("hardware reset")
        self.reset_pin.value = 1
        time.sleep(0.050)
        self.reset_pin.value = 0
        time.sleep(0.002)
        self.reset_pin.value = 1
        time.sleep(0.050)

    def send_command(self, command: int, data: int | bytearray | None = None):
        # SPIDevice automatically sets and clears the chip select pin as needed
        with SPIDevice(self.spi_bus, chip_select=self.cs_pin, baudrate=self.spi_baudrate) as sd:
            # send command
            self.dc_pin.value = 0
            sd.write(bytearray([command]))
            # send data
            if data is None:
                pass  # nothing to do
            elif isinstance(data, int):
                self.dc_pin.value = 1
                sd.write(bytearray([data]))
            elif isinstance(data, bytearray):
                self.dc_pin.value = 1
                sd.write(data)
            else:
                raise ValueError('usage error - invalid type for data')

    def read_busy(self):
        #  0: idle, 1: busy
        while self.busy_pin.value == 1:
            # print("e-Paper busy")
            time.sleep(0.010)
        print("e-Paper busy release")

    def turn_on_display(self):
        self.send_command(0x22, 0xC7)  # DISPLAY_UPDATE_CONTROL_2
        self.send_command(0x20)        # MASTER_ACTIVATION
        self.read_busy()

    def turn_on_display_partial(self):
        self.send_command(0x22, 0x0F)  # DISPLAY_UPDATE_CONTROL_2
        self.send_command(0x20)        # MASTER_ACTIVATION
        self.read_busy()

    def set_lut(self, lut: LookupTable):
        # update lookup table
        self.send_command(0x32, lut.lut)
        self.read_busy()
        # unknown purpose
        self.send_command(0x3f, lut.unk1)
        # gate voltage
        self.send_command(0x03, lut.gate)
        # source voltage (VSH, VSH2, VSL)
        self.send_command(0x04, lut.src)
        # VCOM
        self.send_command(0x2c, lut.vcom)

    def set_window(self, start: waveshare.canvas.Point, end: waveshare.canvas.Point):
        # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_command(0x44, bytearray([(start.x >> 3) & 0xFF, (end.x >> 3) & 0xFF]))
        # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_command(0x45, bytearray([start.y & 0xFF, (start.y >> 8) & 0xFF, end.y & 0xFF, (end.y >> 8) & 0xFF]))

    def set_cursor(self, point: waveshare.canvas.Point):
        # SET_RAM_X_ADDRESS_COUNTER
        self.send_command(0x4E, point.x & 0xFF)
        # SET_RAM_Y_ADDRESS_COUNTER
        self.send_command(0x4F, bytearray([point.y & 0xFF, (point.y >> 8) & 0xFF]))
        self.read_busy()

    def sleep(self):
        self.send_command(0x10, 0x01)  # DEEP_SLEEP_MODE
        time.sleep(2.0)
        self.reset_pin.value = 0
