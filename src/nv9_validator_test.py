import time

from validators.nv9_validator import NV9Validator
from core.test_session import TestSession
from data_logging.event_logger import EventLogger


validator = NV9Validator()

try:
    print("Attempting to connect to NV9...")

    validator.connect()

    print("Connected:", validator.connected)

    print("\nValidator information:")

    serial_number = validator.get_serial_number()
    firmware = validator.get_firmware_version()
    dataset = validator.get_dataset_version()

    print("Serial:", serial_number)
    print("Firmware:", firmware)
    print("Dataset:", dataset)

    setup = validator.get_setup()

    print("\nSetup response:")
    print(setup["raw_hex"])

    channel_map = validator.get_channel_map()

    print("\nChannel map:")

    for channel, details in channel_map.items():
        print(
            f"Channel {channel}: "
            f"{details['value']} "
            f"{details['currency']}"
        )

    session = TestSession(
        test_id="TEST-001",
        validator_model="NV9USB",
        serial_number=serial_number,
        firmware=firmware,
        dataset=dataset,
        operator="Richard",
    )

    logger = EventLogger(
        "validator_events.csv",
        session=session,
    )

    print("\nTest session created:")
    print(session.as_dict())

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

                record = logger.log_event(event)

                print(
                    "Logged:",
                    record["timestamp"],
                    "Test:",
                    record["test_id"]
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