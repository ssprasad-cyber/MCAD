import json
import os
from datetime import datetime


class Logger:
    """Append training metrics to a JSON results file."""

    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump([], f)

    def log(self, record: dict):
        record["timestamp"] = datetime.now().isoformat()

        with open(self.path, "r") as f:
            records = json.load(f)

        records.append(record)

        with open(self.path, "w") as f:
            json.dump(records, f, indent=2)
