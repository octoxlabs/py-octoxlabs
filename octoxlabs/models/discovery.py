# Standard Library
from datetime import datetime
from dataclasses import dataclass

# Octoxlabs
from octoxlabs.utils import parse_string_datetime

DISCOVERY_STATUSES = {1: "Running", 2: "Done", 3: "Error"}


@dataclass
class Discovery:
    id: int
    start_time: str
    end_time: str
    status: int
    progress: float

    @property
    def hr_status(self):
        return DISCOVERY_STATUSES.get(self.status)

    @property
    def parsed_start_time(self) -> datetime:
        return parse_string_datetime(string=self.start_time)

    @property
    def parsed_end_time(self) -> datetime:
        return parse_string_datetime(string=self.end_time)
