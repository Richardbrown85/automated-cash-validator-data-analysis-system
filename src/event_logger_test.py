from data_logging.event_logger import EventLogger


logger = EventLogger("test_validator_events.csv")

test_event = {
    "event_type": "NOTE_CREDIT",
    "event_code": "EE",
    "channel": 2,
    "value": None,
    "currency": None,
    "raw_hex": "7F 00 04 F0 EE 02 CC E0 C2",
}

record = logger.log_event(test_event)

print("Event logged:")
print(record)