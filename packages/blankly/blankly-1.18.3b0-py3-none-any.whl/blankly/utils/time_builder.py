"""
    Time building utils function for easy second building
    Copyright (C) 2021  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Union
from numpy import int64, int32


def build_second() -> int:
    return 1


def build_minute() -> int:
    return build_second() * 60


def build_hour() -> int:
    return build_minute() * 60


def build_day() -> int:
    return build_hour() * 24


def build_week() -> int:
    return build_day() * 7


def build_month() -> int:
    return build_day() * 30


def build_year() -> int:
    return build_day() * 365


def build_decade() -> int:
    return build_year() * 10


def build_century() -> int:
    return build_decade() * 10


def build_millennium() -> int:
    return build_century() * 10


def time_interval_to_seconds(interval: Union[str, float]) -> float:
    """
    Extract the number of seconds in an interval string
    """
    if isinstance(interval, float) or isinstance(interval, int) or isinstance(interval, int64) or \
            isinstance(interval, int32):
        return float(interval)
    # Extract intervals
    if 'mo' in interval:
        interval = interval.replace('mo', 'M')
    try:
        magnitude = int(interval[:-1])
    except ValueError:
        raise ValueError("Invalid time interval definition.")
    unit = interval[-1]

    # Switch units
    if unit == "s":
        base_unit = build_second()
    elif unit == "m":
        base_unit = build_minute()
    elif unit == "h":
        base_unit = build_hour()
    elif unit == "d":
        base_unit = build_day()
    elif unit == "w":
        base_unit = build_week()
    elif unit == "M":
        base_unit = build_month()
    elif unit == "y":
        base_unit = build_year()
    elif unit == "D":
        base_unit = build_decade()
    elif unit == "c":
        base_unit = build_century()
    elif unit == "l":
        base_unit = build_millennium()
    else:
        raise ValueError("Invalid time interval definition.")

    # Scale by the magnitude
    return float(base_unit * magnitude)


def number_interval_to_string(interval: int) -> str:
    """
    This function converts integer intervals into string intervals

    Example: 3600 -> 1h

    Args:
        interval: An integer representing the conversion time
    """
    times = {
        'mo': build_month(),
        'wk': build_week(),
        'd': build_day(),
        'h': build_hour(),
        'm': build_minute(),
        's': build_second()
    }

    unit = None

    for i in times:
        if interval % times[i] == 0:
            unit = i
            break

    magnitude = int(interval/times[unit])

    return f'{magnitude}{unit}'
