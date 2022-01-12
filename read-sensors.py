# -*- coding: utf-8 -*-
# import many libraries
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials
import bme280
import bh1750
import datetime
import config

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

def update_sheet(sheetname, temperature, pressure, humidity, light):
    """update_sheet method:
       appends a row of a sheet in the spreadsheet with the
       the latest temperature, pressure, humidity, and light sensor data
    """
    # authentication, authorization step
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    creds = ServiceAccountCredentials.from_json_keyfile_name(
            'sheets-api-credentials.json', SCOPES)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API, append the next row of sensor data
    # values is the array of rows we are updating, its a single row
    values = [ [
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        temperature,
        pressure,
        humidity,
        light
    ] ]
    body = { 'values': values }
    # call the append API to perform the operation
    result = service.spreadsheets().values().append(
                spreadsheetId=config.SPREADSHEET_ID,
                range=sheetname + '!A1:D1',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body).execute()


def main():
    """main method:
       reads the BME280 and BH1750 chips then
       calls update_sheet method to add their sensor data to the spreadsheet
    """
    bme = bme280.Bme280()
    bme.set_mode(bme280.MODE_FORCED)
    tempC, pressure, humidity = bme.get_data()
    light = round(bh1750.readLight())
    tempF = round((tempC * 9/5) + 32)
    pressure = round(pressure/100)
    humidity = round(humidity)
    print ("Temperature:", tempF, "°F")
    print ("Pressure:", pressure, "mb")
    print ("Humidity:", humidity, "%RH")
    print ("Light Intensity:", light, "LUX")
    update_sheet(config.SHEET_NAME, tempF, pressure, humidity, light)
    display_readings(tempF, pressure, humidity, light)

if __name__ == '__main__':
    main()
