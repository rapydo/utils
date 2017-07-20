
import re
from utilities.uuid import getUUID, getUUIDfromString


def test():

    # 7de267d0-4680-4530-9861-d3c5204a2e46
    regexp = r"[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"

    u = getUUID()
    assert u is not None
    assert isinstance(u, str)
    assert len(u) == 36
    assert re.match(regexp, u) is not None
    assert u != getUUID()

    u = getUUIDfromString("test")
    assert u is not None
    assert isinstance(u, str)
    assert len(u) == 36
    assert re.match(regexp, u) is not None
    assert u == getUUIDfromString("test")
    assert u != getUUIDfromString("test2")
