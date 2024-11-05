from machine import Pin, SPI, I2C
from utime import sleep
import ustruct
from OV2640_reg import *
from Arducam2640 import Arducam2640
import st7789py as st7789

def read_fifo_burst():
    f = open('image.jpg', 'wb')
    count=0
    lenght=camera.read_fifo_length()
    camera.SPI_CS_LOW()
    camera.set_fifo_burst()
    while True:
        camera.spi_readinto(buffer,start=0,end=once_number)
#        usb_cdc.data.write(buffer)
        f.write(buffer)
        sleep(0.00015)
        count+=once_number
        if count+once_number>lenght:
            count=lenght-count
            camera.spi_readinto(buffer,start=0,end=count)
#            usb_cdc.data.write(buffer)
            f.write(buffer)
            camera.SPI_CS_HIGH()
            camera.clear_fifo_flag()
            break
    f.close()


BMP =0
JPEG=1
RAW =2
ARDUCHIP_TRIG=0x41
CAP_DONE_MASK=0x08

once_number=128
mode = 0
start_capture = 0
stop_flag=0
data_in=0
value_command=0
flag_command=0
imageType = JPEG
buffer=bytearray(once_number)
csPin = 5
cs = Pin(csPin, Pin.OUT)

spi0 = SPI(0,
          baudrate=4000000,
          polarity=0,
          phase=0,
          bits=8,
          firstbit=SPI.MSB,
          sck=Pin(2),
          mosi=Pin(3),
          miso=Pin(4))

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=1000000)

print(i2c.scan())

camera = Arducam2640(imageType, cs, spi0, i2c)
camera.Camera_Detection()
camera.Spi_Test()
camera.Camera_Init()
sleep(1)
camera.set_format(imageType)
camera.clear_fifo_flag()
camera.wrSensorReg16_8(0x3818, 0x81);
camera.wrSensorReg16_8(0x3621, 0xA7);
# camera.set_Special_effects(4)  # BW


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
                    rotation=0,
                    color_order=0)

tft.fill(st7789.BLACK)

mode = 1
start_capture = 1
while mode == 1:
    if start_capture==1:
        camera.flush_fifo();
        camera.clear_fifo_flag();
        camera.start_capture();
        start_capture=0
    if camera.get_bit(ARDUCHIP_TRIG,CAP_DONE_MASK)!=0:
        read_fifo_burst()
        mode=0       

print('Image captured')
