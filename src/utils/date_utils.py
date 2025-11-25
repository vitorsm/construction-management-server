from datetime import datetime

def iso_to_datetime(iso_str: str) -> datetime:
    return datetime.fromisoformat(iso_str)

