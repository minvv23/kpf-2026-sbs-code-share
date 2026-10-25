"""날짜 처리."""
from datetime import date, datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))


def today_kst() -> date:
    return datetime.now(KST).date()


def parse_date(value) -> date:
    """'YYYYMMDD', 'YYYY-MM-DD', date 객체를 받는다. 비어 있으면 오늘."""
    if value in (None, ""):
        return today_kst()
    if isinstance(value, date):
        return value
    s = str(value).strip().replace("-", "").replace(".", "")
    return datetime.strptime(s, "%Y%m%d").date()


def yyyymmdd(d: date | None = None) -> str:
    return (d or today_kst()).strftime("%Y%m%d")
