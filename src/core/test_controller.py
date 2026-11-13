from core.test_session import TestSession
from data_logging.event_logger import EventLogger


class TestController:
    """
    Controls a validator test session.

    This keeps validator communication, test metadata,
    event logging and start/stop behaviour away from the UI.
    """

    def __init__(self, validator):
        self.validator = validator

        self.session = None
        self.logger = None

        self.running = False

        self.serial_number = None
        self.firmware = None
        self.dataset = None
        self.validator_model = None
        self.channel_map = {}

    def initialise_validator(self):
        """
        Connect to the validator and read its configuration.
        """

        self.validator.connect()

        self.serial_number = (
            self.validator.get_serial_number()
        )

        self.firmware = (
            self.validator.get_firmware_version()
        )

        self.dataset = (
            self.validator.get_dataset_version()
        )

        self.validator_model = (
            self.validator.get_model_name()
        )

        self.channel_map = (
            self.validator.get_channel_map()
        )

        return self.get_validator_info()

    def get_validator_info(self):
        return {
            "model": self.validator_model,
            "serial_number": self.serial_number,
            "firmware": self.firmware,
            "dataset": self.dataset,
            "port": self.validator.port,
            "channel_map": self.channel_map,
        }

    def start_test(
        self,
        job_id,
        test_id,
        operator,
        filename="validator_events.csv",
    ):
        if self.running:
            raise RuntimeError(
                "A test is already running."
            )

        if not self.validator.connected:
            self.initialise_validator()

        self.session = TestSession(
            job_id=job_id,
            test_id=test_id,
            validator_model=self.validator_model,
            serial_number=self.serial_number,
            firmware=self.firmware,
            dataset=self.dataset,
            operator=operator,
        )

        self.logger = EventLogger(
            filename=filename,
            session=self.session,
        )

        self.validator.enable()

        self.running = True

        return self.session.as_dict()

    def poll_once(self):
        if not self.running:
            raise RuntimeError(
                "No test is currently running."
            )

        result = self.validator.poll()

        for event in result["events"]:
            self.logger.log_event(event)

        return result

    def stop_test(self):
        if not self.running:
            return

        try:
            if self.validator.enabled:
                self.validator.disable()
        finally:
            self.validator.disconnect()

            self.running = False

    def is_running(self):
        return self.running