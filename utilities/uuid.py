# -*- coding: utf-8 -*-

"""
Handling IDs in a more secure way
"""

import uuid

from utilities.logs import get_logger

log = get_logger(__name__)


log.warning(
    "Deprecated import of utilities.uuid, replace with restapi.utilities.uuid")


def getUUID():
    return str(uuid.uuid4())


def getUUIDfromString(string):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, string))
