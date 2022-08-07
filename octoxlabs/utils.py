# Standard Library
from datetime import datetime


def parse_string_datetime(string: str) -> datetime:
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%fZ")
