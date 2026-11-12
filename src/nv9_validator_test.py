from validators.nv9_validator import NV9Validator


validator = NV9Validator()

try:
    print("Attempting to connect to NV9...")

    validator.connect()

    print("Connected:", validator.connected)

    print("\nReading validator information...")

    serial_number = validator.get_serial_number()
    firmware = validator.get_firmware_version()
    dataset = validator.get_dataset_version()

    print("Serial:", serial_number)
    print("Firmware:", firmware)
    print("Dataset:", dataset)

finally:
    validator.disconnect()