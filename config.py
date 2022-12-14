"""file to contain all configurations within the program."""

# used to set the i2c frequency
board_baud_rate = 115200

# for node_mcu, connected scl pin
scl_pin = 4

# for node_mcu, connected sda pin
sda_pin = 5 

# defines time in seconds between reading
time_between_readings = 60

# UTC offset time for seattle
# follows this example: https://bhave.sh/micropython-ntp/
UTC_OFFSET = -8 * 60 * 60