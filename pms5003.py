"""class to manage pms5003 for micropython.  The intent is this controls 
interaction with the PMS5003 sensor for NodeMCU (ESP8266) for micropython
and allows manual access along with automatic reading

# References
1. https://github.com/adafruit/Adafruit_CircuitPython_PM25/blob/master/adafruit_pm25/uart.py
"""

import uos
import machine
from machine import UART
from time import sleep
import struct
import ujson
import urequests
import secrets
import config

def get_reading():
    print('get_reading')
    uos.dupterm(None, 1)
    uart = UART(0)
    uart.init(9600, bits=8, parity=None, stop=1, timeout=1000, timeout_char=2000)
    counter = 0
    counter_limit = 50
    buffer = bytearray(32)
    while True:
        output = uart.read(1)
        datastr = ''.join([chr(b) for b in output])
        if not output:
            raise RuntimeError('unable to read from PMS5003')
        
        if output[0] == 0x42:
            break	

        print(output)	

    buffer[0] = output[0]
    remain = uart.read(31)
    if not remain or len(remain) != 31:
        raise RuntimeError("Unable to read from PM2.5 (incomplete frame)")
    buffer[1:] = remain
    print(buffer)
    
    if not buffer[0:2] == b"BM":
        raise RuntimeError("Invalid PM2.5 header")
        
    frame_len = struct.unpack(">H", buffer[2:4])[0]
    if frame_len != 28:
        raise RuntimeError("Invalid PM2.5 frame length")
        
    checksum = struct.unpack(">H", buffer[30:32])[0]
    check = sum(buffer[0:30])
    aqi_reading = {
            "pm10 standard": None,
            "pm25 standard": None,
            "pm100 standard": None,
            "pm10 env": None,
            "pm25 env": None,
            "pm100 env": None,
            "particles 03um": None,
            "particles 05um": None,
            "particles 10um": None,
            "particles 25um": None,
            "particles 50um": None,
            "particles 100um": None,}
    
    (aqi_reading["pm10 standard"],
    aqi_reading["pm25 standard"],
    aqi_reading["pm100 standard"],
    aqi_reading["pm10 env"],
    aqi_reading["pm25 env"],
    aqi_reading["pm100 env"],
    aqi_reading["particles 03um"],
    aqi_reading["particles 05um"],
    aqi_reading["particles 10um"],
    aqi_reading["particles 25um"],
    aqi_reading["particles 50um"],
    aqi_reading["particles 100um"]
        ) = struct.unpack(">HHHHHHHHHHHH", buffer[4:28])
    
    uos.dupterm(UART(0, 115200), 1)
    return aqi_reading

def get_average_reading(n=5):
    """gets an average reading"""
    print('get average reading function')
    raw_data = []
    for i in range(n):
        raw_data.append(get_reading())
        print(raw_data)
        sleep(2)
    
    pm25_data = [i['pm25 env'] for i in raw_data]
    pm25_calc = int(sum(pm25_data) / len(pm25_data))

    pm10_data = [i['pm10 env'] for i in raw_data]
    pm10_calc = int(sum(pm10_data) / len(pm10_data))

    pm100_data = [i['pm100 env'] for i in raw_data]
    pm100_calc = int(sum(pm100_data) / len(pm100_data))
    
    return {'pm25': pm25_calc, 'pm10': pm10_calc, 'pm100': pm100_calc}

def main():
    """runs process for readings"""
    #uos.dupterm(None, 1)

    results = []

    for i in range(10):
        try:
            results.append(get_reading())
            sleep(5)
        except:
            print('did not work')


    #uos.dupterm(UART(0, 115200), 1)
    return results

def main_out():
    """writes results to text file"""
    for i in range(10):
        try:
            data = get_reading()
            f = open('data.txt', 'a')
            f.write(str(data))
            f.close()
            sleep(5)
        except:
            print('no')

def send_data(reading):
    """sends the dict data to the adafruit IO

    assume reading is provided with dict with pm25, pm10, pm100 fields"""
    # post data
    URL = 0
    data_field = 1
    base_url = 'https://io.adafruit.com'

    mapper = [('/api/v2/{}/feeds/air-quality-pm25/data', 'pm25'),
            ('/api/v2/{}/feeds/air-quality-pm10/data', 'pm10'),
            ('/api/v2/{}/feeds/air-quality-pm100/data', 'pm100')]
    for item in mapper:
        url = base_url + item[URL].format(secrets.ADAFRUIT_IO_USERNAME)
        headers = {'x-aio-key': secrets.ADAFRUIT_IO_KEY,
                'Content-Type': 'application/json',
                }
        data = {'value': reading[item[data_field]]}
        urequests.post(url=url, headers=headers, data=ujson.dumps(data))

def process_data(n=5):
    # put PMS to normal mode
    print("getting average data")
    data = get_average_reading(n=n)
    print("sending data")
    
    return send_data(data)

def set_pms5003_active():
    """sets the pms 5003 active by setting pin high"""
    pass
