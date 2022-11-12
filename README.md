# Tempature Sensor
This builds a temperature reader with teh adafruit [SHT40 reader](https://learn.adafruit.com/adafruit-sht40-temperature-humidity-sensor). This is basic setup which provides terminal readout from the sensor.  

## Node MCU Setup With Micropython
This article provides a nice summary of setting up NodeMCU with micropython.  This should work for blank NodeMCU or one with material already.  https://www.embedded-robotics.com/esp8266-micropython/.  

This provides very good setup and I suggest using Thonny app for develompent.  https://www.embedded-robotics.com/esp8266-micropython/

## ???

To start, I am setting up the NodeMCU with fresh micropython.  I am going to use 
[this reference](https://icircuit.net/nodemcu-getting-started-micropython/2406) to to complete the setup. My setup is on Linux, so here is some helpful howtos on setup:

- how to check drivers on linux `ls /dev/tty*`
- https://www.embedded-robotics.com/esp8266-micropython/
- use `esptool` to flash the board (https://blog.anavi.technology/?p=209)
- to interact with the controller through the usb, get the ampy tool. This is detailed out here https://www.digikey.com/en/maker/projects/micropython-basics-load-files-run-code/fb1fcedaf11e4547943abfdd8ad825ce but can be installed with pip with `pip install adafruit-ampy --upgrade`.  Useful commands are:
  - ls /dev/tty* 
  - ampy --port /dev/ttyUSB0 ls

## Setup
### secrets.py
To set this up, you will need to creat a file on the controller called `secrets.py`.  This contains wifi
connection detail and adafruit IO configuration.  DO NOT ADD this to config control.  

The following is an example secrets defining what is needed.  

```python
# connections is a list of tuples
# the first entry into the tupple is the wifi name
# and the second entry is the password
connections = [('wifi_connection_name_01', 'example_wifi_password'),
               ('wifi_connection_name_02', 'another_example_wifi_password'),
               ]

# connection details for adafruit IO
# reference: https://io.adafruit.com/     
ADAFRUIT_IO_USERNAME = "adafruit_io_username"
ADAFRUIT_IO_KEY = "adafruit_io_apikey"
```

# Parts
* [Adafruit SHT40](https://learn.adafruit.com/adafruit-sht40-temperature-humidity-sensor)

# References
1. [NodeMCU Micropython setup](https://icircuit.net/nodemcu-getting-started-micropython/2406)
2. [Adafruit SHT40 Tutorial](https://learn.adafruit.com/adafruit-sht40-temperature-humidity-sensor)
3. [Micropython setup instructions](https://docs.micropython.org/en/latest/develop/gettingstarted.html)
4. [Instructions for flashing nodemcu](https://www.embedded-robotics.com/esp8266-micropython/)
5. [Micropython downloads for esp8266](https://micropython.org/download/esp8266/)
6. [SHT40 datasheet](https://cdn-learn.adafruit.com/assets/assets/000/099/223/original/Sensirion_Humidity_Sensors_SHT4x_Datasheet.pdf?1612388531)
7. [adafruit circuit python sht40](https://github.com/adafruit/Adafruit_CircuitPython_SHT4x)