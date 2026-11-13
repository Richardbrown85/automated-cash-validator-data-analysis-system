from datetime import datetime


class TestSession:
    def __init__(
        self,
        job_id,
        test_id,
        validator_model,
        serial_number,
        firmware,
        dataset,
        operator=None,
    ):
        self.job_id = job_id
        self.test_id = test_id
        self.validator_model = validator_model
        self.serial_number = serial_number
        self.firmware = firmware
        self.dataset = dataset
        self.operator = operator

        self.start_time = datetime.now().isoformat(
            timespec="milliseconds"
        )

    def as_dict(self):
        return {
            "job_id": self.job_id,
            "test_id": self.test_id,
            "test_start": self.start_time,
            "validator_model": self.validator_model,
            "serial_number": self.serial_number,
            "firmware": self.firmware,
            "dataset": self.dataset,
            "operator": self.operator,
        }