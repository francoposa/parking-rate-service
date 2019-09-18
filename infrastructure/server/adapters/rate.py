import datetime
from typing import Iterable, Mapping, List

import pytz

from usecases.resources.rate import Rate

TIME_FMT = "%H%M"

"""Maps weekday abbreviations into integers
    compatible with Python datetime module
    """
WEEKDAY_STR_TO_INT_MAP = {
    "mon": 0,
    "tues": 1,
    "wed": 2,
    "thurs": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}


def deserialize_rates(json_rates: Iterable[Mapping]) -> List[Rate]:
    """Converts loaded json to Rate usecase objects

    Assumes json-loaded list of rate objects like:
    {
        "days": "mon,tues,thurs",
        "times": "0900-2100",
        "tz": "America/Chicago",
        "price": 1500
    }
    """
    rates: List[Rate] = []
    for json_rate in json_rates:
        times: List[str] = json_rate["times"].split("-")
        start_time: datetime.time = _load_time(times[0], json_rate["tz"])
        end_time: datetime.time = _load_time(times[1], json_rate["tz"])
        days = json_rate["days"].split(",")
        for day_name in days:
            weekday: int = WEEKDAY_STR_TO_INT_MAP[day_name]
            rate = Rate(
                weekday=weekday,
                start_time=start_time,
                end_time=end_time,
                price=json_rate["price"],
            )
            rates.append(rate)
    return rates


def _load_time(time: str, timezone: str) -> datetime.time:
    dt = datetime.datetime.strptime(time, TIME_FMT)
    tz = pytz.timezone(timezone)
    return datetime.time(hour=dt.hour, minute=dt.minute, tzinfo=tz)
