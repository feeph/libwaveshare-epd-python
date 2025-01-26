# Compatibility

The modules for Raspberry Pi and Raspberry Pico are wired differently and
the pinout is not compatible even when using a Pico->Pi breakout board.

## Raspberry Pico

Please note:
- There is no dedicated 'power' pin. The reset pin is used to wake up,
  suspend and reset the display.
- Board power is provided via pin 36 `3V3(OUT)` or pin 39 `VSYS` depending
  on how the board is jumpered.
- Ground is commoned to all 'GND' pins.

__TODO:__
 - confirm if power pin is device dependent

compatible examples:

- [Waveshare Pico e-Paper 2.9](https://www.waveshare.com/wiki/Pico-ePaper-2.9) (296x128, black/white, touchpad)
  - ✓ [Pico_ePaper-2.9.py](https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.9.py)
  - ✗ [Pico_ePaper-2.9-B.py](https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.9-B.py)
  - ✓ [Pico_ePaper-2.9-B_V4.py](https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.9-B_V4.py)
  - ✗ [Pico_ePaper-2.9-C.py](https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.9-C.py)
  - ✗ [Pico_ePaper-2.9_D.py](https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.9_D.py)
- [Waveshare Pico e-Paper 2.9 (B)](https://www.waveshare.com/wiki/Pico-ePaper-2.9-B) (296x128, black/white/red)
- [Waveshare Pico e-Paper 2.9 D](https://www.waveshare.com/wiki/Pico-ePaper-2.9-D) (296x128, black/white)

### logical pinout

for "Pico e-Paper 2.9" (all models)

| pin | GPIO | direction | purpose                        | label |
|-----|------|-----------|--------------------------------|-------|
| GND |      |           | ground                         | GND   |
| 11  | GP8  | output    | data/command select            | DC    |
| 12  | GP9  | output    | SPI1 chip select (SPI1_CSn)    | CS    |
| 14  | GP10 | output    | SPI clock (SPI1_SCK)           | CLK   |
| 15  | GP11 | output    | SPI data in (SPI1_TX)          | DIN   |
| 16  | GP12 | output    | reset                          | RST   |
| 17  | GP13 | input     | busy signal                    | BUSY  |
| 37  |      |           | supply voltage (3.3V)          | VCC   |
| 39  |      |           | supply voltage (VSYS)          | VCC   |

### physical pinout

```
            +---+
      +--+  |USB|  +--+
      | 1|  +---+  |40|
      | 2|         |39| VCC (VSYS)
  GND | 3|         |38| GND
      | 4|         |37| VCC (3V3)
      | 5|         |36|
      | 6|         |35| 
      | 7|         |34|
  GND | 8|         |33| GND
      | 9|         |32| 
      |10|         |31|
   DC |11|         |30| 
   CS |12|         |29| 
  GND |13|         |28| GND
  CLK |14|         |27|
  DIN |15|         |26|
  RST |16|         |25|
  BSY |17|         |24|
  GND |18|         |23| GND
      |19|         |22|
      |20|         |21|
      +--+         +--+
```

## Raspberry Pi (and similar)

__TODO:__
 - confirm VCC is provided via pin 1 (could also be pin 17)
 - confirm GND is provided via pin 39 (could be any other ground pin)

### logical pinout

| pin | GPIO | direction | purpose                        | label |
|-----|------|-----------|--------------------------------|-------|
|  1  |      |           | supply voltage (3.3V)          | VCC   |
| 11  | GP17 | output    | reset                          | RST   |
| 12  | GP18 | output    | power down                     | PWR   |
| 18  | GP24 | input     | busy signal                    | BUSY  |
| 19  | GP10 | output    | SPI0 data in (MOSI)            | DIN   |
| 22  | GP25 | output    | data/command select            | DC    |
| 23  | GP11 | output    | SPI0 clock (SCK)               | CLK   |
| 24  | GP8  | output    | SPI0 chip select #0 (SPI0_CS0) | CS    |
| 39  |      |           | ground                         | GND   |

### physical pinout (40 pin GPIO header)

```
       +-------+
 VCC   |  1  2 |
       |  3  4 |
       |  5  6 |
       |  7  8 |
       |  9 10 |
 RST   | 11 12 | PWR
       | 13 14 |
       | 15 16 |
       | 17 18 | BUSY
 DIN    ┐19 20 |
        ┘21 22 | DC
 CLK   | 23 24 | CS
       | 25 26 |
       | 27 28 |
       | 29 30 |
       | 31 32 |
       | 33 34 |
       | 35 36 |
       | 37 38 |
 GND   | 39 40 |
       +-------+
   board edge ->
```

All modules use the same physical pins for the SPI bus (19, 23, 24) but they may be labeled differently.

### SPI on Jetson Nano

- The module uses the SPI0 bus.
- The SPI bus is provided by shared library `sysfs_software_spi.so`

pinout:

![Jetson Nano pinout](images/646984561.png)
source: https://developer.nvidia.com/embedded/learn/jetson-nano-2gb-devkit-user-guide

### SPI on Raspberry Pi

- The module uses the SPI0 bus.
- SPI bus is provided by Python library `spidev`.

pinout: https://pinout.xyz/

### SPI on Sunrise X3

- The module uses the SPI2 bus. This is the same as SPI0 on Raspberry Pi. It's just labelled differently.
- SPI bus is provided by Python library `spidev`.

pinout:

![Sunrise X3 pinout](images/v2-506c9c20dc0f844915fa86db71fd09e2_b.jpg)

source: https://zhuanlan.zhihu.com/p/579814312
