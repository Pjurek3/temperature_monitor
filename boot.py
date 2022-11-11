import gc
#import webrepl
#webrepl.start()
gc.collect()

import network
import time
import machine


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
        raise OSError('Connection could not be made.\n')