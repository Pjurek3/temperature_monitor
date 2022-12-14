import gc
import network
import machine
import struct
import sys
import time

from adafruit_io import AdafruitIO
from sht40_micropython import SHT40, __version__

import secrets
import config

# this is used to allow us to skip the loop and allow direct access to repl
# if pin 14 is broght low (normally high), then we automatically go to repl
# this avoids long delays due to normal deep sleep mode
skip_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

    
if skip_pin.value() < 1:
  print('repl pin is set.... exiting to repl and skipping program')
  sys.exit()


# this controls what I do in the script.  This will determine if i go to repl, continue or deep sleep
sta_if = network.WLAN(network.STA_IF)
connected_check = sta_if



def deep_sleep(msecs):
  #configure RTC.ALARM0 to be able to wake the device
  # thank you to: https://randomnerdtutorials.com/micropython-esp8266-deep-sleep-wake-up-sources/
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
  # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
  rtc.alarm(rtc.ALARM0, msecs)
  #put the device to sleep
  machine.deepsleep()



# this will deep sleed if the wifi is not connected and we don't have repl pin set
if not sta_if.isconnected():
  deep_sleep(30 * 60 * 1000)



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

    wdt = machine.WDT()  # enable it with a timeout of 2s
    wdt.feed()
    results = sht40.measure()
    wdt.feed()
    """
    with open('data.txt', 'a+') as f:
        f.write('{}, {}, {}\n'.format(results[0], results[1], time.localtime()))
    """
    aio.send(value=results[0], url = url_humidity)
    wdt.feed()
    aio.send(value=results[1], url = url_temperature)
    led.value(1)
    wdt.feed()
    gc.collect()
    # multiply by 1000 to convert expected input to seconds since function expects ms
    deep_sleep(config.time_between_readings*1000)
