# WeatherLogger

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149386111-5d8a14da-db21-44b3-976c-2ffa7c7eb3ba.jpg" width="100%" height="100%">
</p>

Instructions and python code for turning a raspberry pi plus sensors and display into a weather station that logs readings to a Google sheet.

#### Table of Contents

[Step 1: Tools and Materials](#tools-and-materials)<br>
[Step 2: Set up Pi](#set-up-pi)<br>
[Step 3: Solder](#solder)<br>
[Step 4: Connect sensors](#connect-sensors)<br>
[Step 5: Test sensors](#test-sensors)<br>
[Step 6: Set up remote logging](#set-up-remote-logging)<br>
[Step 7: Final assembly](#final-assembly)<br>

Links to the original [BME280](https://github.com/cmur2/python-bme280) and [BH1750](https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bh1750.py) python libraries. Credit to [Allan Schwartz's blog](http://www.whatimade.today/log-sensor-data-straight-to-google-sheets-from-a-raspberry-pi-zero-all-the-python-code/) for the idea and the sheets api submission code.

# Tools and Materials

Tools:

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149386269-46a58690-5016-403c-8a2d-96cca660f7ca.jpg" width="50%" height="50%">
</p>

- Drill and Bits
- Soldering Iron
- Breadboard
- Micro SD card adapter
- Utility Knife


Materials:

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149386383-61a19f27-b65f-4ea4-a8e2-4baedad0c66b.jpg" width="75%" height="75%">
</p>

- [Raspberry Pi Zero W plus power cable](https://amzn.to/36XpZBv)
- [8GB or more Micro SD card](https://amzn.to/2YXBOTR)
- [BME280 sensor](https://amzn.to/2N6lDRt)
- [BH1750 sensor](https://amzn.to/2Z0b6ds)
- [I2C OLED display](https://amzn.to/2YUIVfM)
- Female to Female Dupont Wire
- Breakaway male header pins
- White Electrical Tape and/or Duct Tape
- Epoxy
- [White S11 LED light bulb cover](https://amzn.to/3q2a4Jz)
- 1/2 inch pvc cap
- Electronics Solder
- A plastic jar with a white lid
- Aluminium Foil


# Set up Pi

Connect the SD card to a computer using the adapter, and flash it with latest raspberry pi OS using raspberry pi imager.

The Lite version of the OS is sufficient. Once flashed but before ejecting navigate to the newly created `/boot` dir and run `touch ssh` to enable ssh.

Also create a file called `wpa_supplicant.conf` in the `/boot` dir and add the following lines, editing to fit your wireless network's details

```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
        ssid="mySSID"
        psk="myPassword"
        key_mgmt=WPA-PSK
}
```

This will connect your pi to wifi on booot, enabling headless wireless networking.
More details [here](http://www.whatimade.today/when-the-pi-goes-stale-we-bake-another/#creatingthemicrosdcard).

# Solder

Solder the header pins that came with each sensor to the sensor itself. Solder five male header pins to the pi's pins 1,3,5,7, and 9.

Create a dupont wire hub by breaking away 4 header pins and soldering them together. Repeat this 4 times for a total of 4 hubs.

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149387200-6737ed30-141f-4c5a-978d-38e020136f2f.jpg" width="90%" height="100%">
</p>

# Connect sensors

Wire pi to sensors via:
- Wire color 1 from pi pin 1 and sensors/display VIN to hub 1
- Wire color 2 from pi pin 3 and sensors/display SDA to hub 2
- Wire color 3 from pi pin 5 and sensors/display SCL to hub 3
- Wire color 4 from pi pin 9 and sensors/display GND to hub 4

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149387703-ea0963c3-0525-4e53-a66a-8a0b589f707b.jpg" width="50%" height="50%">
</p>

Insulate the exposed solder on each hub with electrical tape. Also join/wrap each set of female connecters with electrical tape.

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149387797-4d537ce2-a283-4088-8c89-ca3109b827df.jpg" width="50%" height="50%">
</p>

Insert the SD card into the pi zero W's slot and connect the power cable.

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149388226-6f56da81-35a4-41de-83fa-22739fc7146f.jpg" width="75%" height="75%">
</p>

# Test sensors

Switch on the power to boot up the pi zero w. Use a smartphone + Network Scanner app (or a computer and the nmap utility) to find the pi's IP address.

Connect to it via SSH (`ssh pi@your.ip.add.ress`) and:
- Change the pi's password to something other than the default (which is `raspberry`).
- Use raspi-config to set language, timezone, and enable i2c.
- run `sudo apt-get install -y i2c-tools python3-smbus python-pip python-pil git` to install python-smbus, i2c-tools, pip, pil, and git if not already installed.
- run `sudo pip3 install adafruit-circuitpython-ssd1306`
- run `pip install --upgrade google-api-python-client oauth2client` to install google api python client
- Reboot using `sudo reboot`, then connect again via ssh and run `i2cdetect -y 1` to verify the sensors and display are properly connected.

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149408573-23d1baf8-233f-49a4-b2e5-668421d4dfea.png" width="50%" height="50%">
</p>

- Clone to this repo to the pi home dir with git `git clone https://github.com/bellerbrock/WeatherLogger.git`, then
cd into it with `cd WeatherLogger`
- run `python -c "from read_sensors import demo; demo()"` to test sensors. You should see output in your console, and matching readings on the OLED display

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149408608-c60309da-7e97-4b57-a475-3c9ee1938804.png" width="75%" height="75%">
</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149388305-bc6d7a20-55a8-4286-92a4-d740014d64bf.jpg" width="75%" height="75%">
</p>

# Set up remote logging

Create a Google sheet. Copy the sheet name and id into the config.py file.
Follow [google's instructions](https://gspread.readthedocs.io/en/latest/oauth2.html) to enable api access for logging. Currently they are:
- Go to Google Developers Console and create a new project.
- In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it.
- In the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it.
- Go to “APIs & Services > Credentials” and choose “Create credentials > Service account key”.
- Fill out the form, click “Create key”, and select “JSON” and click “Create”.

You will automatically download a JSON file with credentials. Open the file, copy the value of 'client_email' in the file, then go to your google sheet and share it with the client email.

Next copy the JSON credential file to the pi zero WeatherLogger repo and name it `sheets-api-credentials.json`.
Run `python read_sensors.py` to test logging.
Once working run `crontab -e` and add a line like `
*/5 * * * * cd /home/pi/project/WeatherLogger; python read_sensors.py` for automatic logging (in this case every 5 mins).

# Final assembly

Shutdown the pi.
Drill a hole in the center of the lid of your jar, large enough to fit the pi power cable.
Drill three smaller holes evenly spaced around the edges of the lid, then use a utility knife to expand them into slots large enough to fit the dupont wire hubs for the sensors.
Drill holes for airflow in the sides of the pvc cap, slanting them slightly upwards.
Reassemble the components with the pi in the jar and the sensors on top of the lid. Seal the lid penetrations with white tape.

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149390928-c926defc-76d3-4f58-b90d-c0f235c458f9.jpg" width="75%" height="75%">
</p>

Use Epoxy to fix the pvc cover on top of the BME280 sensor and the light bulb cover on top of the BH1750 sensor.
Cut a matching slot in the bottom of the clear plastic OLED display case, then connect the display inside it's case and use epoxy to fix it to the lid
Protect the internal components from overheating/ direct sunlight. Wrap aluminum foil around the jar and secure it with tape.

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149391101-85ded00e-b406-4a4e-aa9f-e714f0b16a7a.jpg" width="75%" height="75%">
</p>

Finally, hang the pi in it's final location. Connect it to power, restart it, and watch the data roll in!

<p align="center">
<img src="https://user-images.githubusercontent.com/11297346/149391148-2e0176b4-8300-4c59-9ab5-4550246de369.jpg" width="75%" height="75%">
</p>
