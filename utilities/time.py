# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
import dateutil.parser

from utilities.logs import get_logger

log = get_logger(__name__)


def timestamp_from_string(timestamp_string):
    """
    Neomodels complains about UTC, this is to fix it.
    Taken from http://stackoverflow.com/a/21952077/2114395
    """

    precision = float(timestamp_string)
    # return datetime.fromtimestamp(precision)

    utc_dt = datetime.utcfromtimestamp(precision)
    aware_utc_dt = utc_dt.replace(tzinfo=pytz.utc)

    return aware_utc_dt


def date_from_string(date, format="%d/%m/%Y"):

    if date == "":
        return ""
    # datetime.now(pytz.utc)
    try:
        return_date = datetime.strptime(date, format)
    except BaseException:
        return_date = dateutil.parser.parse(date)

    return pytz.utc.localize(return_date)


def string_from_timestamp(timestamp):
    if timestamp == "":
        return ""
    try:
        date = datetime.fromtimestamp(float(timestamp))
        return date.isoformat()
    except BaseException:
        log.warning("Errors parsing %s" % timestamp)
        return ""
