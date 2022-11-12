import machine
import struct
import time

from adafruit_io import AdafruitIO
from sht40_micropython import SHT40, __version__

import secrets
import config

# scl -> yellow wire
# sda -> blue wire
# reference: https://learn.adafruit.com/assets/99229

# pin GPIO5 -> d1
# pin GPI04 -> d2

led = machine.Pin(2, machine.Pin.OUT)

sht40 = SHT40(scl_pin=config.scl_pin, sda_pin=config.sda_pin, freq=config.board_baud_rate)
results = sht40.measure()

print('version: {}'.format(__version__))
print('temperature: {0:.3g}C'.format(results[1]))
print('humidity: {0:.3g}%'.format(results[0]))

aio = AdafruitIO(username=secrets.ADAFRUIT_IO_USERNAME, key=secrets.ADAFRUIT_IO_KEY)

url_temperature = '/feeds/office-temperature.office-temperature/data'
url_humidity = '/feeds/office-temperature.office-humidity/data'

while True:


    # turning light on to start
    led.value(0)

    results = sht40.measure()
    aio.send(value=results[0], url = url_humidity)
    aio.send(value=results[1], url = url_temperature)
    led.value(1)

    time.sleep(config.time_between_readings)