import datetime
from abc import ABCMeta, abstractmethod
from typing import Iterable, Optional

from app.usecases.resources.rate import Rate


class IRateRepo(metaclass=ABCMeta):
    """Define expected behavior for a datastore of Rates"""

    class TimeRangeError(Exception):
        """Raised upon receipt of an invalid time range for a rate lookup"""

    @abstractmethod
    async def set_rates(self, rates: Iterable[Rate]) -> None:
        """Clobber rate data with new set of rates"""

    @abstractmethod
    async def get_rate_for_time_range(
        self, start_time: datetime.datetime, end_time: datetime.datetime
    ) -> Optional[Rate]:
        """Get rate [if any] that completely encapsulate the given time range

        Raise TimeRangeError for invalid start - end time ranges
        """
