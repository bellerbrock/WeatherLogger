# -*- coding: utf-8 -*-
from __future__ import print_function
import bme280
import bh1750
import datetime
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

def display_readings(temperature, pressure, humidity, light):
    """display_readings method:
       diplays the latest sensor readings on the lcd display, along with timestamp and ip address  
    """
    

    # Raspberry Pi pin configuration:
    RST = None     # on the PiOLED this pin isnt used
    # Note the following are only used with SPI:
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    # 128x32 display with hardware I2C:
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0


    # Load default font.
    font = ImageFont.load_default()

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

    # Write two lines of text.
    line1 = str(temperature) + " F" + "  " + str(pressure) + " mb"
    line2 = str(humidity) + " %" + "  " + str(light) + " lux"
    draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
    draw.text((x, top+8),     str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")), font=font, fill=255)
    draw.text((x, top+16),    line1,  font=font, fill=255)
    draw.text((x, top+25),    line2,  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()


def main():
    bme = bme280.Bme280()
    bme.set_mode(bme280.MODE_FORCED)
    tempC, pressure, humidity = bme.get_data()
    light = round(bh1750.readLight())
    tempF = round((tempC * 9/5) + 32)
    pressure = round(pressure/100)
    humidity = round(humidity)
    print ("Temperature:", tempF, "°F")
    print ("Pressure:", pressure, "mb")
    print ("Humidity:", humidity, "%%rH")
    print ("Light Intensity:", light, "lux")
    display_readings(tempF, pressure, humidity, light)

if __name__ == '__main__':
    main()
