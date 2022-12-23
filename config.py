"""file to contain all configurations within the program."""

__version__ = '0.0.6'
__repo__ = 'tbd'

# used to set the i2c frequency
board_baud_rate = 115200

# for node_mcu, connected scl pin
scl_pin = 4

# for node_mcu, connected sda pin
sda_pin = 5 

# defines time in seconds between reading
time_between_readings = 180

# temp until we refactor
sleep_time = time_between_readings

# UTC offset time for seattle
# follows this example: https://bhave.sh/micropython-ntp/
UTC_OFFSET = -8 * 60 * 60

# number of data points to average on each reading
avg_data_points = 5 

pms5003_pins = {'set': 14,
                            }