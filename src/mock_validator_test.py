from validators.mock_validator import MockValidator


validator = MockValidator()

validator.connect()

print("Serial:", validator.get_serial_number())
print("Firmware:", validator.get_firmware_version())
print("Dataset:", validator.get_dataset_version())

validator.enable()

events = validator.poll()

print("Events:", events)

validator.disable()
validator.disconnect()