import csv
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


class EventLogger:
    def __init__(
        self,
        filename=None,
        session=None,
    ):
        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        if filename is None or filename == "":
            self.filename = DATA_DIR / "validator_events.csv"
        else:
            self.filename = Path(filename)

        self.session = session

        self.fieldnames = [
            "job_id",
            "test_id",
            "test_start",
            "timestamp",
            "validator_model",
            "serial_number",
            "firmware",
            "dataset",
            "operator",
            "event_type",
            "event_code",
            "channel",
            "value",
            "currency",
            "raw_hex",
        ]

        self._create_file_if_needed()

    def _create_file_if_needed(self):
        if not self.filename.exists():
            with self.filename.open(
                "w",
                newline="",
                encoding="utf-8",
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames,
                )
                writer.writeheader()

    def log_event(self, event):
        session_data = {}

        if self.session is not None:
            session_data = self.session.as_dict()

        record = {
            "job_id": session_data.get("job_id"),
            "test_id": session_data.get("test_id"),
            "test_start": session_data.get("test_start"),
            "timestamp": datetime.now().isoformat(
                timespec="milliseconds"
            ),
            "validator_model": session_data.get(
                "validator_model"
            ),
            "serial_number": session_data.get(
                "serial_number"
            ),
            "firmware": session_data.get("firmware"),
            "dataset": session_data.get("dataset"),
            "operator": session_data.get("operator"),
            "event_type": event["event_type"],
            "event_code": event["event_code"],
            "channel": event["channel"],
            "value": event["value"],
            "currency": event["currency"],
            "raw_hex": event["raw_hex"],
        }

        with self.filename.open(
            "a",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=self.fieldnames,
            )
            writer.writerow(record)

        return record