from datetime import time

import attr
from attr.validators import instance_of


@attr.s(frozen=True)
class Rate:
    """Represents a parking rate

    A rate is for a given weekday
    rate in effect beginning start_time inclusive
    rate in effect until end_time exclusive
    """

    weekday: int = attr.ib(validator=instance_of(int))
    start_time: time = attr.ib(validator=instance_of(time))
    end_time: time = attr.ib(validator=instance_of(time))
    price: int = attr.ib(validator=instance_of(int))
