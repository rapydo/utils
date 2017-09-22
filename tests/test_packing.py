# -*- coding: utf-8 -*-

import pytest
from utilities.packing import install
from utilities.packing import list_all
from utilities.packing import check_version


def test():

    packages = list_all()
    assert packages is not None
    assert isinstance(packages, list)
    assert len(packages) > 0

    found = False
    for pkg in packages:
        if pkg._key == "rapydo-utils":
            found = True

    if not found:
        pytest.fail("rapydo.utils not found in the list of packages")

    ver = check_version("rapydo-utils")
    assert ver is not None

    ver = check_version("rapydo-blabla")
    assert ver is None

    install("docker-compose")
