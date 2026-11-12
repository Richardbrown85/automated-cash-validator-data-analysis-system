from validators.nv9_validator import NV9Validator


validator = NV9Validator()

print("NV9Validator created successfully.")
print("Port:", validator.port)
print("Baud rate:", validator.baud_rate)
print("Connected:", validator.connected)
print("Enabled:", validator.enabled)