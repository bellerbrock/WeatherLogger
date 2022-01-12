# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import time
import subprocess
import board
import bme280
import bh1750
import adafruit_ssd1306
import digitalio
from PIL import Image, ImageDraw, ImageFont

def display_readings(temperature, pressure, humidity, light):
    """display_readings method:
       diplays the latest sensor readings on the lcd display, along with timestamp and ip address
    """

    # Define the Reset Pin
    oled_reset = digitalio.DigitalInOut(board.D4)

    # Define dimensions
    WIDTH = 128
    HEIGHT = 32
    top = -2
    x = 0

    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    # Clear display.
    oled.fill(0)
    oled.show()

    # Create blank image for drawing.
    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Load default font.
    font = ImageFont.load_default()

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True ).strip().decode( "utf-8" )

    # Create two lines of sensor text.
    line1 = str(temperature) + " F" + "    " + str(pressure) + " mb"
    line2 = str(humidity) + " %RH" + "  " + str(light) + " LUX"

    draw.text((x, top),       str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")), font=font, fill=255)
    draw.text((x, top+8),     line1,  font=font, fill=255)
    draw.text((x, top+16),    line2,  font=font, fill=255)
    draw.text((x, top+25),    "IP: " + str(IP),  font=font, fill=255)

    # Display image.
    oled.image(image)
    oled.show()


def main():
    bme = bme280.Bme280()
    bme.set_mode(bme280.MODE_FORCED)
    tempC, pressure, humidity = bme.get_data()
    light = round(bh1750.readLight())
    tempF = round((tempC * 9/5) + 32)
    pressure = round(pressure/100)
    humidity = round(humidity)
    print ("Temperature:", tempF, "F")
    print ("Pressure:", pressure, "mb")
    print ("Humidity:", humidity, "%RH")
    print ("Light Intensity:", light, "LUX")
    display_readings(tempF, pressure, humidity, light)

if __name__ == '__main__':
    main()
