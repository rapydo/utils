# -*- coding: utf-8 -*-

from utilities.time import timestamp_from_string
from utilities.time import date_from_string
from utilities.time import string_from_timestamp
from utilities.time import get_online_utc_time
from datetime import datetime
from dateutil.tz import tzutc
import pytz
import pytest


def test():

    test_timestamp = "423423423"
    t = timestamp_from_string(test_timestamp)

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

    d1 = date_from_string('06/07/2018')
    d2 = date_from_string('2018-07-06', fmt='%Y-%m-%d')

    assert d1 == d2
    # UTC is defaulted for non-localized dates
    assert d1.tzinfo == pytz.utc

    d = date_from_string('')
    assert d == ""

    d = date_from_string('2017-09-22T07:10:35.822772835Z')
    assert d.tzinfo == tzutc()

    d = date_from_string('2017-09-22T07:10:35.822772835+01:00')
    assert d.tzinfo != tzutc()
    assert d.tzinfo is not None

    d = string_from_timestamp('')
    assert d == ""

    d = string_from_timestamp("not-float-value")
    assert d == ""

    d = string_from_timestamp(test_timestamp)
    # Isoformat expected
    assert d == '1983-06-02T19:37:03'

    # Just to call it... what to verify?
    get_online_utc_time()
