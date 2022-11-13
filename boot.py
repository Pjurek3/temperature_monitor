import gc
#import webrepl
#webrepl.start()
gc.collect()

import network
import time
import machine
import ntptime

def deep_sleep(msecs):
  #configure RTC.ALARM0 to be able to wake the device
  # thank you to: https://randomnerdtutorials.com/micropython-esp8266-deep-sleep-wake-up-sources/
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
  # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
  rtc.alarm(rtc.ALARM0, msecs)
  #put the device to sleep
  machine.deepsleep()


sta_if = network.WLAN(network.STA_IF); 
sta_if.active(True)

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

try:
    from secrets import connections
except OSError:
    raise OSError('No secrets file found!')


for connection in connections:
    station, password = connection

    print("Connecting to {}.".format(station))

    sta_if.connect(station, password)

    for i in range(15):
        print(".")

        if sta_if.isconnected():
            break

        time.sleep(1)

    if sta_if.isconnected():
        break
    else:
        print('Connection could not be made... going to sleep for 30 minutes')
        deep_sleep(30 * 60 * 1000)


# TODO -> figure out how to sync this with my timezone
ntptime.settime()