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

# My Spreadsheet ID ... See google documentation on how to derive this
MY_SPREADSHEET_ID = '1BMW1JmsHRVQTZn7ggFSDVjr4XCiD5GLGWmTcXA6szXE'


def update_sheet(sheetname, temperature, pressure, humidity, sunlight):
    """update_sheet method:
       appends a row of a sheet in the spreadsheet with the
       the latest temperature, pressure, humidity, and sunlight sensor data
    """
    # authentication, authorization step
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    creds = ServiceAccountCredentials.from_json_keyfile_name(
            'sheets-api-credentials.json', SCOPES)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API, append the next row of sensor data
    # values is the array of rows we are updating, its a single row
    values = [ [ str(datetime.datetime.now()), temperature, pressure, humidity, sunlight] ]
    body = { 'values': values }
    # call the append API to perform the operation
    result = service.spreadsheets().values().append(
                spreadsheetId=MY_SPREADSHEET_ID,
                range=sheetname + '!A1:G1',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body).execute()


def main():
    """main method:
       reads the BME280 and BH1750 chips then
       calls update_sheets method to add their sensor data to the spreadsheet
    """
    bme = bme280.Bme280()
    bme.set_mode(bme280.MODE_FORCED)
    tempC, pressure, humidity = bme.get_data()
    sunlight = bh1750.readLight()
    tempF = (tempC * 9/5) + 32
    pressure = pressure/100.
    print ('Temperature: %f °F' % tempF)
    print ('Pressure: %f mb' % pressure)
    print ('Humidity: %f %%rH' % humidity)
    print ('Sunlight: %f lux' % sunlight)
    update_sheet("Sunroom", tempF, pressure, humidity, sunlight)


if __name__ == '__main__':
    main()
