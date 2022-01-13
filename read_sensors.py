# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import time
import subprocess
import board
import config

import bme280
import bh1750
import adafruit_ssd1306
import digitalio

from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials


def retrieve_readings():
    """retrieve_readings method:
       retrieves sensor values for temperature, pressure, humidity, and light
       returns values in dictionary format, rounded to nearest sig fig
    """
    bme = bme280.Bme280()
    bme.set_mode(bme280.MODE_FORCED)
    tempC, pressure, humidity = bme.get_data()
    return {
        'tempF': round((tempC * 9/5) + 32),
        'pressure': round(pressure/100),
        'humidity': round(humidity),
        'light': round(bh1750.readLight())
    }


def print_readings(readings):
    """print_readings method:
       prints readings to STDOUT
    """
    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    print ("Temperature:", readings["tempF"], "°F")
    print ("Pressure:", readings["pressure"], "mb")
    print ("Humidity:", readings["humidity"], "%%RH")
    print ("Light Intensity:", readings["light"], "LUX")


def display_readings(readings):
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
    line1 = str(readings["tempF"]) + " F" + "    " + str(readings["pressure"]) + " mb"
    line2 = str(readings["humidity"]) + " %RH" + "  " + str(readings["light"]) + " LUX"

    draw.text((x, top),       str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")), font=font, fill=255)
    draw.text((x, top+8),     line1,  font=font, fill=255)
    draw.text((x, top+16),    line2,  font=font, fill=255)
    draw.text((x, top+25),    "IP: " + str(IP),  font=font, fill=255)

    # Display image.
    oled.image(image)
    oled.show()


def update_sheet(sheetname, readings):
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
        readings["tempF"],
        readings["pressure"],
        readings["humidity"],
        readings["light"]
    ] ]
    body = { 'values': values }
    # call the append API to perform the operation
    result = service.spreadsheets().values().append(
                spreadsheetId=config.SPREADSHEET_ID,
                range=sheetname + '!A1:D1',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body).execute()


def demo():
    """demo method:
       retrieves readings, prints them to STDOUT, and displays them on the station's oled screen
    """
    readings = retrieve_readings()
    print_readings(readings)
    display_readings(readings)


def main():
    """main method:
       retrieves readings, displays them on the station's oled screen and
       logs them to the google spreadsheet
    """
    readings = retrieve_readings()
    display_readings(readings)
    update_sheet(config.SHEET_NAME, readings)

if __name__ == '__main__':
    main()
