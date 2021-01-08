# WeatherLogger
Instructions and python code for turning a raspberry pi plus sensors into a weather station that logs readings to a Google sheet.

Original [BME280 python library](https://github.com/cmur2/python-bme280) and [BH1750 library](https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bh1750.py). Credit to [Allan Schwartz's blog](http://www.whatimade.today/log-sensor-data-straight-to-google-sheets-from-a-raspberry-pi-zero-all-the-python-code/) for the idea and the sheets api submission code.

# Tools and Materials

Tools: 
- Crimping Pliers
- Wire Stripper and Cutter
- Soldering Iron
- Drill and Bits
- Multimeter/Continuity Tester
- Breadboard

Materials:
- Raspberry Pi Zero W plus micro SD card and power cable
- BME280 sensor
- BH1750 sensor
- Wire
- Female Dupont Connectors
- Electrical Tape
- Electronics Solder
- Plastic Jar
- Twine
- Aluminium Foil

# Step 1: Set up Pi Zero W

Flash SD card with latest raspberry pi os using raspberry pi imager.
Once flashed but before ejecting enable ssh and add wpa_supplicant file for headless wireless networking.
More details [here](http://www.whatimade.today/when-the-pi-goes-stale-we-bake-another/#creatingthemicrosdcard)

# Step 2: Make wires

Make four Y-shaped wires with female dupont adapters. Nice guide [here](https://www.mschoeffler.de/2017/12/26/diy-y-adapter-jumper-wire/) One each of Red, Black, White, and Grey.
Use continuity test to make aure double crimped wires are working.
Use Dupont housing if it works, electrical tape if it doesn't.

# Step 3: Solder

Solder header pins that came with sensors to the sensors, and five pins to pi pins 1,3,5,7,9. More details for BME260 [here](http://www.whatimade.today/log-sensor-data-straight-to-google-sheets-from-a-raspberry-pi-zero-all-the-python-code/#hardware)
Use breadboard if needed for stability.

# Step 4: Connect for testing

Wire pi to sensors via:
- Red wire from pi pin 1 to sensors VIN
- Grey wire from pi pin 3 to sensors SDA
- White wire from pi pin 5 to sensors SCL
- Black wire from pi pin 9 to sensors GND

Insert SD card into pi zero w's slot.
Connect pi power cable.

# Step 5: Test

Boot up pi zero w. Use Network Scanner to find pi's IP address and connect to it via SSH.
Change pi's default password. Use raspi-config to set language, timezone, and enable i2c.
install python-smbus and i2c-tools if not already installed.
reboot and run i2cdetect -y 1 to verify both sensors are working.
Use git clone to copy this repo to the pi.
run `python demo.y` to test sensors.

# Step 6: Set up logging via API

Create a Google sheet. Copy the sheet name and id into the config.py file.
Install google api python client `pip install --upgrade google-api-python-client oauth2client`
Follow [google's instructions](https://gspread.readthedocs.io/en/latest/oauth2.html) to enable api access for logging. Currently they are:
- Go to Google Developers Console and create a new project.
- In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it.
- In the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it.
- Go to “APIs & Services > Credentials” and choose “Create credentials > Service account key”.
- Fill out the form, click “Create key”, and select “JSON” and click “Create”.

You will automatically download a JSON file with credentials. Copy to the pi zero WeatherLogger repo and name it sheets-api-credentials.json.
Run `python read-sensors.py` to test logging.
Once working run `crontab -e` and add a line like `
*/5 * * * * cd /home/pi/project/WeatherLogger; python read-sensors.py` for automatic logging (in this case every 5 mins). 

# Step 7: Final assembly

Shutdown the pi.
Drill a hole in the bottom of your jar for the pi power cable and the center of the top for the sensor wires.
Drill a couple extra holes in the top to run twine thorugh for hanging.
Reassemble the pi in the jar and the sensors on top of the lid. If deployed outside or in direct sunlight add protection. For example aluminum foil around the jar to protect the pi, a semi-transparent dome for the BH1750 sensor, a cover with air circulation for the BME280.
Restart the pi and watch the data roll in.

