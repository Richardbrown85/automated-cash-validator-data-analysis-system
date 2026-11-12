from validators.nv9_validator import NV9Validator


validator = NV9Validator()

try:
    print("Attempting to connect to NV9...")

    validator.connect()

    print("Connected:", validator.connected)

    print("\nReading validator information...")

    print("Serial:", validator.get_serial_number())
    print("Firmware:", validator.get_firmware_version())
    print("Dataset:", validator.get_dataset_version())

    print("\nEnabling validator...")

    validator.enable()

    print("Enabled:", validator.enabled)

    print("\nPolling NV9...")

    result = validator.poll()

    print("Poll result:", result)

finally:
    if validator.connected:
        try:
            if validator.enabled:
                validator.disable()
        finally:
            validator.disconnect()