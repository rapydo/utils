# -*- coding: utf-8 -*-

import pytest
from utilities.logs import handle_log_output
from utilities.logs import re_obscure_pattern

from utilities.logs import get_logger

log = get_logger(__name__)

# from utilities import apiclient
# log = apiclient.setup_logger(name=__name__, level_name='very_verbose')
# # log.warning("DEBUG TRAVIS", log)


def test(capfd):

    TESTING_MESSAGE = "Let's test the output!"

    log.very_verbose(TESTING_MESSAGE)
    log.verbose(TESTING_MESSAGE)
    log.debug(TESTING_MESSAGE)
    log.info(TESTING_MESSAGE)
    log.warning(TESTING_MESSAGE)
    log.error(TESTING_MESSAGE)

    log.checked(TESTING_MESSAGE)

    log.print_stack(TESTING_MESSAGE)
    log.print(TESTING_MESSAGE)
    log.pp({"test": 123}, prefix_line="test")
    log.fail(TESTING_MESSAGE)

    try:
        log.critical_exit(TESTING_MESSAGE)
    except SystemExit:
        pass
    else:
        pytest.fail("A SystemExit should be raised")

    out, err = capfd.readouterr()
    out = out.split("\n")
    err = err.split("\n")

    log.warning("PRINT TRAVIS LOGGER LEVEL: %s", log)

    # assert ("VERY_VERBOSE %s" % TESTING_MESSAGE) in err
    # assert ("VERBOSE %s" % TESTING_MESSAGE) in err
    # assert ("DEBUG %s" % TESTING_MESSAGE) in err
    assert ("INFO %s" % TESTING_MESSAGE) in err
    assert ("WARNING %s" % TESTING_MESSAGE) in err
    assert ("ERROR %s" % TESTING_MESSAGE) in err
    assert ("ERROR %s" % TESTING_MESSAGE) in err

    # assert ("VERBOSE (CHECKED)\t%s" % TESTING_MESSAGE) in err
    # assert ("VERBOSE \u2713 %s" % TESTING_MESSAGE) in err
    assert ("INFO (CHECKED)\t%s" % TESTING_MESSAGE) in err
    assert ("INFO \u2713 %s" % TESTING_MESSAGE) in err
    assert ("PRINT_STACK %s" % TESTING_MESSAGE) in err
    assert ("ERROR (FAIL)\t%s" % TESTING_MESSAGE) in err
    assert ("EXIT %s" % TESTING_MESSAGE) in err

    log.very_verbose("%s", TESTING_MESSAGE)
    log.verbose("%s", TESTING_MESSAGE)
    log.debug("%s", TESTING_MESSAGE)
    log.info("%s", TESTING_MESSAGE)
    log.warning("%s", TESTING_MESSAGE)
    log.error("%s", TESTING_MESSAGE)

    # assert ("VERY_VERBOSE %s" % TESTING_MESSAGE) in err
    # assert ("VERBOSE %s" % TESTING_MESSAGE) in err
    # assert ("DEBUG %s" % TESTING_MESSAGE) in err
    assert ("INFO %s" % TESTING_MESSAGE) in err
    assert ("WARNING %s" % TESTING_MESSAGE) in err
    assert ("ERROR %s" % TESTING_MESSAGE) in err

    test = re_obscure_pattern("protocol://user:password@host:port")
    assert test == "protocol://user:****@host:port"

    test = handle_log_output(None)
    assert test == {}

    test = handle_log_output("         ".encode("utf-8"))
    assert test == {}

    data = """
            {
                "xyz": "abc",
                "user": "abc",
                "password": "abc",
                "pwd": "abc",
                "token": "abc",
                "file": "abc",
                "filename": "abc"
            }
""".encode(
        "utf-8"
    )
    test = handle_log_output(data)

    assert "xyz" in test
    assert "user" in test
    assert "password" in test
    assert "pwd" in test
    assert "token" in test
    assert "file" in test
    assert "filename" in test

    assert test["xyz"] == "abc"
    assert test["user"] == "abc"
    assert test["password"] == "****"
    assert test["pwd"] == "****"
    assert test["token"] == "****"
    assert test["file"] == "****"
    assert test["filename"] == "****"

    for e in err:
        print(e)
