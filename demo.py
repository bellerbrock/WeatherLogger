# -*- coding: utf-8 -*-
from __future__ import print_function
import bme280
import bh1750


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


if __name__ == '__main__':
    main()
