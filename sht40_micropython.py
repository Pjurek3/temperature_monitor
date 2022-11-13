"""class interface to the sht40 using i2c

this is based off the circuit python version 
https://github.com/adafruit/Adafruit_CircuitPython_SHT4x"""

import machine
import struct
import time

__version__ = '0.0.5'
__repo__ = 'tbd'

_SHT4X_DEFAULT_ADDR = const(0x44)  # SHT4X I2C Address
_SHT4X_READSERIAL = const(0x89)  # Read Out of Serial Register
_SHT4X_SOFTRESET = const(0x94)  # Soft Reset

class SHT40:
    """i2c interafce for the SHT40 sensor
    """

    def __init__(self, scl_pin, sda_pin, freq=115200):
        """interface for SHT40

        Args:
            scl_pin (int): scl pin identifier
            sda_pin (int): sda pin identifier
            freq (int, optional): board frequency based off nodemcu baud rate. Defaults to 115200.
        """

        self.i2c = machine.I2C(scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin), freq=freq)

    def measure(self) -> tuple(float, float):
        """reads hubitity (%) and temperature (C) and returns
        tuple with results.  First value is humidity (0-100 %) and second
        value is temperature (C)
        """
        buffer = bytearray(6)

        # creating this so we can fill it in later.  Following the circuit python
        # example here https://github.com/adafruit/Adafruit_CircuitPython_SHT4x/blob/main/adafruit_sht4x.py
        buffer = bytearray(6)

        # filling in buffer from this standard
        buffer[0] = 0xFD

        # initiating i2c bus
        self.i2c.writeto(_SHT4X_DEFAULT_ADDR, buffer)

        # can adjust this in future
        time.sleep(1)

        # now going to read
        self.i2c.readfrom_into(_SHT4X_DEFAULT_ADDR, buffer)

        temp_data = buffer[0:2]
        temp_crc = buffer[2]
        humidity_data = buffer[3:5]
        humidity_crc = buffer[5]

        temperature = struct.unpack_from(">H", temp_data)[0]
        temperature = -45.0 + 175.0 * temperature / 65535.0
        temperature_f = (temperature * 9/5) +32

        # repeat above steps for humidity data
        humidity = struct.unpack_from(">H", humidity_data)[0]
        humidity = -6.0 + 125.0 * humidity / 65535.0
        humidity = max(min(humidity, 100), 0)

        return (humidity, temperature)
