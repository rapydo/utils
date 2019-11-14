# -*- coding: utf-8 -*-

"""
If you need things globally,
come here and take.
"""

from utilities.logs import get_logger

log = get_logger(__name__)

log.print_stack("")
log.warning(
    "Deprecated import of utilities.globals, replace with restapi.utilities.globals")


class mem:
    """
    Source:
    https://pythonconquerstheuniverse.wordpress.com/
        2010/10/20/a-globals-class-pattern-for-python/
    """

    pass
