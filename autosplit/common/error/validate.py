from typing import Optional

from common.error.exceptions import InvalidOptionException, OutOfRangeOptionException


def validate_int(
    user_input: str, range_min: int = 0, range_max: Optional[int] = None
) -> int:
    try:
        int_input = int(user_input)
        if int_input < range_min or (range_max is not None and int_input > range_max):
            raise OutOfRangeOptionException(option=user_input)
        return int_input
    except ValueError:
        raise InvalidOptionException(option=user_input)
