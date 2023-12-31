from datetime import datetime
from zoneinfo import ZoneInfo

utc_zone = ZoneInfo("UTC")


def as_utc(dt: datetime):
    return dt.replace(tzinfo=utc_zone)


def utcnow():
    now = datetime.utcnow()
    return as_utc(now)
