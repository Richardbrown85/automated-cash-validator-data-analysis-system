from core.test_session import TestSession
from data_logging.event_logger import EventLogger


session = TestSession(
    test_id="TEST-001",
    validator_model="NV9USB",
    serial_number=4294,
    firmware="NVS0091201025000",
    dataset="GBP03022",
    operator="Richard",
)

logger = EventLogger(
    "test_session_events.csv",
    session=session,
)

event = {
    "event_type": "NOTE_CREDIT",
    "event_code": "EE",
    "channel": 2,
    "value": None,
    "currency": None,
    "raw_hex": "7F 00 04 F0 EE 02 CC E0 C2",
}

record = logger.log_event(event)

print("Test session:")
print(session.as_dict())

print("\nLogged event:")
print(record)