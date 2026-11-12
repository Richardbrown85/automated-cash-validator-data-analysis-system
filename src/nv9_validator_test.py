from validators.nv9_validator import NV9Validator


validator = NV9Validator()

try:
    print("Attempting to connect to NV9...")

    validator.connect()

    print("Connected:", validator.connected)

finally:
    validator.disconnect()