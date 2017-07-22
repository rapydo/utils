
import pytest
import os
import logging
from utilities.globals import mem
from utilities.logs import get_logger
log = get_logger(__name__)


def test():

    log.very_verbose("testing")
    log.verbose("testing")
    log.debug("testing")
    log.info("testing")
    log.warning("testing")
    log.error("testing")

    log.checked_simple("testing")
    log.checked("testing")
    # FIXME: this kind of setting should be tested
    mem.action = "check"
    log.checked_simple("testing")
    log.checked("testing")

    log.print_stack("testing")
    log.print("testing")
    log.pp({"test": 123}, prefix_line="test")
    log.fail("testing")

    try:
        log.critical_exit("testing")
    except SystemExit:
        pass
    else:
        pytest.fail("A SystemExit should be raised")

    # FIXME: this kind of setting should be tested
    os.environ['AVOID_COLORS_ENV_LABEL'] = "1"

    # FIXME: this new logger should be tested
    get_logger(__name__)
