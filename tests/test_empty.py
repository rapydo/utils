
from utilities.logs import get_logger
log = get_logger(__name__)


def nextint(x):
    return x + 1


def test_answer():
    assert nextint(3) == 4
    log.info("testing")
