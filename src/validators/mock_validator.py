from .base_validator import BaseValidator


class MockValidator(BaseValidator):
    """
    Simulated cash validator.

    Used for testing the application without requiring
    physical validator hardware.
    """

    def __init__(self):
        self.connected = False
        self.enabled = False

    def connect(self):
        self.connected = True
        print("Mock validator connected.")

    def disconnect(self):
        self.connected = False
        print("Mock validator disconnected.")

    def enable(self):
        if not self.connected:
            raise RuntimeError("Validator is not connected.")

        self.enabled = True
        print("Mock validator enabled.")

    def disable(self):
        self.enabled = False
        print("Mock validator disabled.")

    def poll(self):
        if not self.connected:
            raise RuntimeError("Validator is not connected.")

        if not self.enabled:
            return []

        return [
            {
                "event_type": "NOTE_ACCEPTED",
                "channel": 1,
                "value": 10.00,
                "currency": "GBP"
            }
        ]

    def get_serial_number(self):
        return "MOCK-0001"

    def get_firmware_version(self):
        return "MOCK-FW-1.0"

    def get_dataset_version(self):
        return "MOCK-GBP-1.0"