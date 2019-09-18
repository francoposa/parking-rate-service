import datetime
from typing import Iterable, List, Optional

from app.usecases.interfaces import IRateRepo
from app.usecases.resources.rate import Rate


class InMemoryRateRepo(IRateRepo):
    def __init__(self):
        self._data: List[Rate] = []

    async def set_rates(self, rates: Iterable[Rate]) -> None:
        self._data = [rate for rate in rates]

    async def get_rate_for_time_range(
        self, start_time: datetime.datetime, end_time: datetime.datetime
    ) -> Optional[Rate]:
        self._validate_time_range(start_time, end_time)
        for rate in self._data:
            if rate.weekday == start_time.weekday():
                # Start/end time discrepancies should be validated already
                if (
                    start_time.time() >= rate.start_time
                    and end_time.time() <= rate.end_time
                ):
                    return rate
        return None

    def _validate_time_range(
        self, start_time: datetime.datetime, end_time: datetime.datetime
    ):
        """Checks for validity of start and end times provided.

        Intended to test for rate-agnostic time range logic such as
        - is start time after end time
        - are start time and end time on the same day

        Is not intended to determine whether the time range will produce a search result

        Raise TimeRangeError with relevant message if range is invalid
        Return None otherwise
        """
        if start_time >= end_time:
            raise self.TimeRangeError("start timestamp must be before end timestamp")
        if not start_time.date() == end_time.date():
            raise self.TimeRangeError(
                "start timestamp and end timestamp must be on the same date"
            )
