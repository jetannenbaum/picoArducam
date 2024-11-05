from utime import sleep
import ustruct
from OV2640_reg import *

MAX_FIFO_SIZE=0x7FFFFF
ARDUCHIP_FRAMES=0x01
ARDUCHIP_TIM=0x03
VSYNC_LEVEL_MASK=0x02
ARDUCHIP_TRIG=0x41
CAP_DONE_MASK=0x08

OV2640_160x120  =0
OV2640_176x144  =1
OV2640_320x240  =2
OV2640_352x288  =3
OV2640_640x480  =4
OV2640_800x600  =5
OV2640_1024x768 =6
OV2640_1280x1024=7
OV2640_1600x1200=8

Advanced_AWB =0
Simple_AWB   =1
Manual_day   =2
Manual_A     =3
Manual_cwf   =4
Manual_cloudy=5


degree_180=0
degree_150=1
degree_120=2
degree_90 =3
degree_60 =4
degree_30 =5
degree_0  =6
degree30  =7
degree60  =8
degree90  =9
degree120 =10
degree150 =11

Auto   =0
Sunny  =1
Cloudy =2
Office =3
Home   =4

Antique     =0
Bluish      =1
Greenish    =2
Reddish     =3
BW          =4
Negative    =5
BWnegative  =6
Normal      =7
Sepia       =8
Overexposure=9
Solarize    =10
Blueish     =11
Yellowish   =12

Exposure_17_EV  =0
Exposure_13_EV  =1
Exposure_10_EV  =2
Exposure_07_EV  =3
Exposure_03_EV  =4
Exposure_default=5
Exposure03_EV   =6
Exposure07_EV   =7
Exposure10_EV   =8
Exposure13_EV   =9
Exposure17_EV   =10

Auto_Sharpness_default=0
Auto_Sharpness1       =1
Auto_Sharpness2       =2
Manual_Sharpnessoff   =3
Manual_Sharpness1     =4
Manual_Sharpness2     =5
Manual_Sharpness3     =6
Manual_Sharpness4     =7
Manual_Sharpness5     =8

MIRROR     =0
FLIP       =1
MIRROR_FLIP=2

Saturation4 =0
Saturation3 =1
Saturation2 =2
Saturation1 =3
Saturation0 =4
Saturation_1=5
Saturation_2=6
Saturation_3=7
Saturation_4=8

Brightness4 =0
Brightness3 =1
Brightness2 =2
Brightness1 =3
Brightness0 =4
Brightness_1=5
Brightness_2=6
Brightness_3=7
Brightness_4=8

Contrast4 =0
Contrast3 =1
Contrast2 =2
Contrast1 =3
Contrast0 =4
Contrast_1=5
Contrast_2=6
Contrast_3=7
Contrast_4=8

Antique      = 0
Bluish       = 1
Greenish     = 2
Reddish      = 3
BW           = 4
Negative     = 5
BWnegative   = 6
Normal       = 7
Sepia        = 8
Overexposure = 9
Solarize     = 10
Blueish      = 11
Yellowish    = 12

high_quality   =0
default_quality=1
low_quality    =2

Color_bar   =0
Color_square=1
BW_square   =2
DLI         =3

BMP =0
JPEG=1
RAW =2

class Arducam2640(object):
    def __init__(self, mode, cs, spi, i2c):
        self.CameraMode=mode
        self.cs=cs
        self.SPI_CS_HIGH()
        self.I2cAddress=0x30
        self.spi = spi
        self.i2c = i2c
        self.Spi_write(0x07,0x80)
        sleep(0.1)
        self.Spi_write(0x07,0x00)
        sleep(0.1)
        
    def Camera_Detection(self):
        self.wrSensorReg8_8(0xff,0x01)
        id_h=self.rdSensorReg8_8(0x0a)
        id_l=self.rdSensorReg8_8(0x0b)
        if(id_h==b'\x26')and((id_l==b'\x40')or(id_l==b'\x42')):
            print('CameraType is OV2640')
        else:
            print('Can\'t find OV2640 module', hex(ord(id_h)), hex(ord(id_l)))
            
    def Set_Camera_mode(self,mode):
        self.CameraMode=mode

    def wrSensorReg8_8(self,addr,val):
        buffer=bytearray(2)
        buffer[0]=addr
        buffer[1]=val
        self.i2c.writeto(self.I2cAddress, buffer)

    def wrSensorRegs8_8(self,reg_value):
        for data in reg_value:
            addr = data[0]
            val = data[1]
            if (addr == 0xff and val == 0xff):
                return
            self.wrSensorReg8_8(addr, val)
            sleep(0.001)
            
    def wrSensorReg16_8(self,addr,val):
        buffer=bytearray(3)
        buffer[0]=(addr>>8)&0xff
        buffer[1]=addr&0xff
        buffer[2]=val
        self.i2c.writeto(self.I2cAddress, buffer)
        sleep(0.003)
            
    def wrSensorRegs16_8(self,reg_value):
        for data in reg_value:
            addr = data[0]
            val = data[1]
            if (addr == 0xffff and val == 0xff):
                return
            self.wrSensorReg16_8(addr, val)

    def rdSensorReg8_8(self,addr):
        return self.i2c.readfrom_mem(self.I2cAddress, addr, 1)

    def SPI_CS_LOW(self):
        self.cs.value(False)
        
    def SPI_CS_HIGH(self):
        self.cs.value(True)

    def Spi_write(self,address,value):
        maskbits = 0x80
        buffer=bytearray(2)
        buffer[0]=address|maskbits
        buffer[1]=value
        self.SPI_CS_LOW()
        self.spi.write(buffer)
        self.SPI_CS_HIGH()
        
    def Spi_read(self,address):
        maskbits = 0x7F
        buffer=bytearray(1)
        buffer[0]=address&maskbits
        self.SPI_CS_LOW()
        self.spi.write(buffer)
        buffer = self.spi.read(1)
        self.SPI_CS_HIGH()
        return buffer
    
    def get_bit(self,addr,bit):
        value=self.Spi_read(addr)[0]
        return value&bit
        
    def Spi_Test(self):
        while True:
            self.Spi_write(0X00,0X56)
            value=self.Spi_read(0X00)
            if(value[0]==0X56):
                print('SPI interface OK')
                break
            else:
                print('SPI interface Error')
            utime.sleep(1)

    def Camera_Init(self):
        self.wrSensorReg8_8(0xff,0x01)
        self.wrSensorReg8_8(0x12,0x80)
        sleep(0.1)
        self.wrSensorRegs8_8(OV2640_JPEG_INIT);
        self.wrSensorRegs8_8(OV2640_YUV422);
        self.wrSensorRegs8_8(OV2640_JPEG);
        self.wrSensorReg8_8(0xff,0x01)
        self.wrSensorReg8_8(0x15,0x00)
        self.wrSensorRegs8_8(OV2640_320x240_JPEG);

    def clear_fifo_flag(self):
        self.Spi_write(0x04,0x01)
        
    def flush_fifo(self):
        self.Spi_write(0x04,0x01)
        
    def start_capture(self):
        self.Spi_write(0x04,0x02)
        
    def read_fifo_length(self):
        len1=self.Spi_read(0x42)[0]
        len2=self.Spi_read(0x43)[0]
        len3=self.Spi_read(0x44)[0]
        len3=len3 & 0x7f
        lenght=((len3<<16)|(len2<<8)|(len1))& 0x07fffff
        return lenght

    def set_fifo_burst(self):
        buffer=bytearray(1)
        buffer[0]=0x3c
        self.spi_write(buffer, start=0, end=1)
        
    def set_format(self,mode):
        if mode==BMP or mode==JPEG or mode==RAW:   
            self.CameraMode=mode

    def spi_write(self, buf, *, start=0, end=None):
        if end is None:
            end = len(buf)
        self.spi.write(buf)
        
    def spi_readinto(self, buf, *, start=0, end=None):
        if end is None:
            end = len(buf)
        self.spi.readinto(buf)

    def set_Special_effects(self,Special_effect):
        if Special_effect== Antique:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x40)
            self.wrSensorReg8_8(0x7d, 0xa6)
        elif Special_effect== Bluish:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0xa0)
            self.wrSensorReg8_8(0x7d, 0x40)
        elif Special_effect== Greenish:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x40)
            self.wrSensorReg8_8(0x7d, 0x40)
        elif Special_effect== Reddish:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x40)
            self.wrSensorReg8_8(0x7d, 0xc0)
        elif Special_effect== BW:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x18)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x80)
            self.wrSensorReg8_8(0x7d, 0x80)
        elif Special_effect== Negative:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x40)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x80)
            self.wrSensorReg8_8(0x7d, 0x80)
        elif Special_effect== BWnegative:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x58)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x80)
            self.wrSensorReg8_8(0x7d, 0x80)
        elif Special_effect== Normal:
            self.wrSensorReg8_8(0xff, 0x00)
            self.wrSensorReg8_8(0x7c, 0x00)
            self.wrSensorReg8_8(0x7d, 0x00)
            self.wrSensorReg8_8(0x7c, 0x05)
            self.wrSensorReg8_8(0x7d, 0x80)
            self.wrSensorReg8_8(0x7d, 0x80)
