
import pytest
import os
import logging
from utilities.globals import mem
from utilities.logs import get_logger
log = get_logger(__name__)


def test(capfd):

    TESTING_MESSAGE = "Let's test the output!"

    log.very_verbose(TESTING_MESSAGE)
    log.verbose(TESTING_MESSAGE)
    log.debug(TESTING_MESSAGE)
    log.info(TESTING_MESSAGE)
    log.warning(TESTING_MESSAGE)
    log.error(TESTING_MESSAGE)

    log.checked_simple(TESTING_MESSAGE)
    log.checked(TESTING_MESSAGE)
    # FIXME: this kind of setting should be tested
    mem.action = "check"
    log.checked_simple(TESTING_MESSAGE)
    log.checked(TESTING_MESSAGE)

    log.print_stack(TESTING_MESSAGE)
    log.print(TESTING_MESSAGE)
    log.pp({"test": 123}, prefix_line="test")
    log.fail(TESTING_MESSAGE)

    try:
        log.critical_exit(TESTING_MESSAGE)
        pass
    except SystemExit:
        pass
    else:
        pytest.fail("A SystemExit should be raised")

    out, err = capfd.readouterr()
    out = out.split("\n")
    err = err.split("\n")

    assert ("VERY_VERBOSE %s" % TESTING_MESSAGE) in err
    assert ("VERBOSE %s" % TESTING_MESSAGE) in err
    assert ("DEBUG %s" % TESTING_MESSAGE) in err
    assert ("INFO %s" % TESTING_MESSAGE) in err
    assert ("WARNING %s" % TESTING_MESSAGE) in err
    assert ("ERROR %s" % TESTING_MESSAGE) in err
    assert ("ERROR %s" % TESTING_MESSAGE) in err
    assert ("VERBOSE (CHECKED)\t%s" % TESTING_MESSAGE) in err
    assert ("VERBOSE \u2713 %s" % TESTING_MESSAGE) in err
    assert ("INFO (CHECKED)\t%s" % TESTING_MESSAGE) in err
    assert ("INFO \u2713 %s" % TESTING_MESSAGE) in err
    assert ("PRINT_STACK %s" % TESTING_MESSAGE) in err
    assert ("ERROR (FAIL)\t%s" % TESTING_MESSAGE) in err
    assert ("EXIT %s" % TESTING_MESSAGE) in err

    # This syntax should be preferable:
    # Specify string format arguments as logging function parameters

    log.very_verbose("%s", TESTING_MESSAGE)
    log.verbose("%s", TESTING_MESSAGE)
    log.debug("%s", TESTING_MESSAGE)
    log.info("%s", TESTING_MESSAGE)
    log.warning("%s", TESTING_MESSAGE)
    log.error("%s", TESTING_MESSAGE)
    assert ("VERY_VERBOSE %s" % TESTING_MESSAGE) in err
    assert ("VERBOSE %s" % TESTING_MESSAGE) in err
    assert ("DEBUG %s" % TESTING_MESSAGE) in err
    assert ("INFO %s" % TESTING_MESSAGE) in err
    assert ("WARNING %s" % TESTING_MESSAGE) in err
    assert ("ERROR %s" % TESTING_MESSAGE) in err

    for e in err:
        print(e)
