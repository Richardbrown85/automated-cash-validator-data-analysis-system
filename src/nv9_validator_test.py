import time

from validators.nv9_validator import NV9Validator


validator = NV9Validator()

try:
    print("Attempting to connect to NV9...")

    validator.connect()

    print("Connected:", validator.connected)

    print("\nValidator information:")
    print("Serial:", validator.get_serial_number())
    print("Firmware:", validator.get_firmware_version())
    print("Dataset:", validator.get_dataset_version())

    print("\nEnabling validator...")

    validator.enable()

    print("Enabled:", validator.enabled)

    print("\nPolling started.")
    print("Insert a banknote now.")
    print("Press Ctrl+C to stop.\n")

    while True:
        result = validator.poll()

        if result:
         print("POLL:", result["raw_hex"])

        for event in result["events"]:
         print(
            event["event_type"],
            "Channel:",
            event["channel"]
        )

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nPolling stopped by user.")

finally:
    if validator.connected:
        try:
            if validator.enabled:
                validator.disable()
        finally:
            validator.disconnect()