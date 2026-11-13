from utils.serial_port_finder import find_validator_port

VALIDATOR_TYPE = "NV9"
SERIAL_PORT = find_validator_port()

BAUD_RATE = 9600
DATA_BITS = 8
STOP_BITS = 2
PARITY = "NONE"