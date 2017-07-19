
import pytest
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
    log.print_stack("testing")
    log.print("testing")
    log.pp({"test": 123})
    # try:
    #     log.fail_exit("testing")
    # except SystemExit:
    #     pass
    # else:
    #     pytest.fail("A SystemExit should be raised")

    try:
        log.critical_exit("testing")
    except SystemExit:
        pass
    else:
        pytest.fail("A SystemExit should be raised")
