# libwaveshare-epd-python

Python library for Waveshare ePaper Display

The official Waveshare libraries can be found at
https://github.com/waveshareteam/e-Paper (Raspberry Pi) and
https://github.com/waveshareteam/Pico_ePaper_Code (Raspberry Pico)
but the code in these libraries is extremely repetitive (each display size
has it's own implementation).

This library aims to provde a complete reimplementation in a more usable and
maintainable shape.

## code maturity

This library is in alpha stage and very much work in progress. The main
motivation right now is to build an understanding how the various ePaper
devices differ and how to use them correctly.

## ePaper display models

| letter | bits | available colors                               |
| ------ | ---- | ---------------------------------------------- |
| none   | 2    | black, dark gray, light gray, white            |
| B      | 2    | black, red, white                              |
| C      | 2    | black, yellow, white                           |
| D      | 1    | black, white                                   |
| F      | 4    | black, white, green, blue, red, yellow, orange |
| G      | 2    | black, red, yellow, white                      |
| K      | 2    |  black, dark gray, light gray, white           |

### for Raspberry Pi and compatible (Jetson Nano, Sunrise X3, ...)

https://www.waveshare.com/wiki/Main_Page#Display-e-Paper

| model                                                                            | form factor | resolution  | interface | colors                                         | extra features |
| -------------------------------------------------------------------------------- | ----------- | ----------- | --------- | ---------------------------------------------- | -------------- |
| [e-Paper 1.54"](https://www.waveshare.com/wiki/1.54inch_e-Paper_Module)          | module      |   200 × 200 | SPI       | black, white                                   |                |
| [e-Paper 1.54" (B)](https://www.waveshare.com/wiki/1.54inch_e-Paper_Module_(B))  | module      |   200 × 200 | SPI       | black, red, white                              |                |
| [e-Paper 1.54" (C)](https://www.waveshare.com/wiki/1.54inch_e-Paper_Module_(C))  | module      |   152 x 152 | SPI       | black, yellow, white                           |                |
| [e-Paper 2.13"](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT)             | HAT         |   250 × 122 | SPI       | black, white                                   |                |
| [e-Paper 2.13" (B)](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(B))     | HAT         |   250 × 122 | SPI       | black, red, white                              |                |
| [e-Paper 2.13" (C)](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(C))     | HAT         |   250 × 122 | SPI       | black, yellow, white                           |                |
| [e-Paper 2.13" (D)](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(D))     | HAT         |   212 × 104 | SPI       | black, white                                   |                |
| [Touch e-Paper 2.13"](https://www.waveshare.com/wiki/2.13inch_Touch_e-Paper_HAT) | HAT         |   250 × 122 | SPI       | black, white                                   | touchpad       |
| [e-Paper 2.15" (B)](https://www.waveshare.com/wiki/2.15inch_e-Paper_HAT%2B_(B))  | HAT+        |   296 × 160 | SPI       | black, red, white                              |                |
| [e-Paper 2.15" (G)](https://www.waveshare.com/wiki/2.15inch_e-Paper_HAT%2B_(G))  | HAT+        |   296 × 160 | SPI       | black, red, yellow, white                      |                |
| [e-Paper 2.66"](https://www.waveshare.com/wiki/2.66inch_e-Paper_Module)          | module      |   296 × 152?| SPI       | black, white                                   |                |
| [e-Paper 2.66" (B)](https://www.waveshare.com/wiki/2.66inch_e-Paper_Module_(B))  | HAT (Pi)    |   296 × 160 | SPI       | black, red, white                              |                |
| [e-Paper 2.7"](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT)               | HAT (Pi)    |   264 × 176 | SPI       | black, dark gray, light gray, white            |                |
| [e-Paper 2.7" (B)](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_(B))       | HAT (Pi)    |   264 × 176 | SPI       | black, dark gray, light gray, white            |                |
| [e-Paper 2.9"](https://www.waveshare.com/wiki/2.9inch_e-Paper_Module)            | module      |   296 × 128 | SPI       | black, dark gray, light gray, white            |                |
| [e-Paper 2.9" (B)](https://www.waveshare.com/wiki/2.9inch_e-Paper_Module_(B))    | module      |   296 × 128 | SPI       | black, red, white                              |                |
| [e-Paper 2.9" (C)](https://www.waveshare.com/wiki/2.9inch_e-Paper_Module_(C))    | module      |   296 × 128 | SPI       | black, yellow, white                           |                |
| [e-Paper 2.9" (D)](https://www.waveshare.com/wiki/2.9inch_e-Paper_HAT_(D))       | HAT         |   296 × 128 | SPI       | black, white                                   |                |
| [e-Paper 3.52" (B)](https://www.waveshare.com/wiki/3.52inch_e-Paper_HAT_(B))     | HAT         |   360 × 240 | SPI       | black, red, white                              |                |
| [e-Paper 3.7"](https://www.waveshare.com/wiki/3.7inch_e-Paper_HAT)               | HAT         |   480 × 280 | SPI       | black, dark gray, light gray, white            |                |
| [e-Paper 4.01" (F)](https://www.waveshare.com/wiki/4.01inch_e-Paper_HAT_(F))     | HAT         |   640 × 400 | SPI       | black, white, green, blue, red, yellow, orange |                |
| [e-Paper 4.2"](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module)            | module      |   400 × 300 | SPI       | black, dark gray, light gray, white            |                |
| [e-Paper 4.2" (B)](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_(B))    | module      |   400 × 300 | SPI       | black, red, white                              |                |
| [e-Paper 4.2" (C)](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_(C))    | module      |   400 × 300 | SPI       | black, yellow, white                           |                |
| [e-Paper 4.2" (G)](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_(G))    | module      |   400 × 300 | SPI       | black, red, yellow, white                      |                |
| [e-Paper 4.3" UART](https://www.waveshare.com/wiki/4.3inch_e-Paper_UART_Module)  | module      |   800 × 600 | UART      | black, dark gray, light gray, white            |                |
| ...                                                                              |             |             |           |                                                |                |

### for Raspberry Pico

| model                                                                                  | form factor | resolution | interface | colors                              | extra features |
| -------------------------------------------------------------------------------------- | ----------- | ---------- | --------- | ----------------------------------- | -------------- |
| [Pico e-Paper 2.13" (B)](https://www.waveshare.com/wiki/Pico-ePaper-2.13-B)            |             |            |           |                                     |                |
| [Pico e-Paper 2.13" (D)](https://www.waveshare.com/wiki/Pico-ePaper-2.13-D)            |             |            |           |                                     |                |
| [Pico e-Paper 2.13"](https://www.waveshare.com/wiki/Pico-ePaper-2.13)                  |             |            |           |                                     |                |
| [Pico e-Paper 2.66" (B)](https://www.waveshare.com/wiki/Pico-ePaper-2.66-B)            |             |            |           |                                     |                |
| [Pico e-Paper 2.66"](https://www.waveshare.com/wiki/Pico-ePaper-2.66)                  |             |            |           |                                     |                |
| [Pico e-Paper 2.7](https://www.waveshare.com/wiki/Pico-ePaper-2.7)                     |             |            |           |                                     |                |
| [Pico e-Paper 2.9"](https://www.waveshare.com/wiki/Pico-ePaper-2.9)                    | HAT (Pico)  |  296 x 128 | SPI, I2C  | black, dark gray, light gray, white | touchpad       |
| [Pico e-Paper 2.9" (B)](https://www.waveshare.com/wiki/Pico-ePaper-2.9-B)              | HAT (Pico)  |  296 x 128 | SPI       | black, red, white                   |                |
| [Pico e-Paper 2.9" (D)](https://www.waveshare.com/wiki/Pico-ePaper-2.9-D)              | HAT (Pico)  |  296 x 128 | SPI       | black, dark gray, light gray, white | 2 buttons      |
| [Pico CapTouch e-Paper 2.9"](https://www.waveshare.com/wiki/Pico-CapTouch-ePaper-2.9)  |             |            |           |                                     |                |
| [Pico e-Paper 3.7"](https://www.waveshare.com/wiki/Pico-ePaper-3.7)                    |             |            |           |                                     |                |
| [Pico e-Paper 4.2" (B)](https://www.waveshare.com/wiki/Pico-ePaper-4.2-B)              |             |            |           |                                     |                |
| [Pico e-Paper 4.2](https://www.waveshare.com/wiki/Pico-ePaper-4.2)                     |             |            |           |                                     |                |
| [Pico e-Paper 5.65](https://www.waveshare.com/wiki/Pico-ePaper-5.65)                   |             |            |           |                                     |                |
| [Pico e-Paper 5.83" (B)](https://www.waveshare.com/wiki/Pico-ePaper-5.83-B)            |             |            |           |                                     |                |
| [Pico e-Paper 5.83"](https://www.waveshare.com/wiki/Pico-ePaper-5.83)                  |             |            |           |                                     |                |
| [Pico e-Paper 7.5" (B)](https://www.waveshare.com/wiki/Pico-ePaper-7.5-B)              |             |            |           |                                     |                |
| [Pico e-Paper 7.5"](https://www.waveshare.com/wiki/Pico-ePaper-7.5)                    |             |            |           |                                     |                |
