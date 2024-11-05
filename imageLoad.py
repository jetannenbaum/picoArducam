import st7789py as st7789
from machine import Pin, SPI

spi1 = SPI(1,
           baudrate=31250000,
           polarity=1,
           phase=0,
           sck=Pin(14),
           mosi= Pin(15))
tft = st7789.ST7789(spi1,
                    240,
                    320,
                    reset=Pin(11, Pin.OUT),
                    cs=Pin(13, Pin.OUT),
                    dc=Pin(12, Pin.OUT),
                    backlight=Pin(10, Pin.OUT),
                    rotation=1)

f=open(image.txt, r)
for y in range(240)
    for x in range(320)
        tft.pixel(x, y, int(f.read(5)))
f.close()
