import csv
from datetime import datetime
from pathlib import Path


class EventLogger:
    def __init__(self, filename="validator_events.csv"):
        self.filename = Path(filename)

        self.fieldnames = [
            "timestamp",
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
                encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fieldnames
                )
                writer.writeheader()

    def log_event(self, event):
        record = {
            "timestamp": datetime.now().isoformat(
                timespec="milliseconds"
            ),
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
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=self.fieldnames
            )
            writer.writerow(record)

        return record