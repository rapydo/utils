# -*- coding: utf-8 -*-

from utilities.time import timestamp_from_string
from datetime import datetime
import pytz
import pytest


def test():

    t = timestamp_from_string("423423423")

    d = datetime(1983, 6, 2, 17, 37, 3, tzinfo=pytz.utc)
    assert t == d

    try:
        t = timestamp_from_string("asd")
    except ValueError:
        pass
    else:
        pytest.fail("This call should raise a ValueError")

    t = timestamp_from_string("0")
    d = datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    assert t == d

    t = timestamp_from_string("-1")
    d = datetime(1969, 12, 31, 23, 59, 59, tzinfo=pytz.utc)
    assert t == d
