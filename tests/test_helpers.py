# -*- coding: utf-8 -*-

import pytest
from utilities.helpers import (
    list_path,
    last_dir,
    parent_dir,
    root_path,
    script_abspath,
    current_dir,
    module_from_package,
    project_dir,
    # get_api_url,
)


def test():

    p = list_path(".")

    assert p is not None
    assert isinstance(p, list)
    assert len(p) > 0

    try:
        list_path("blabla")
    except FileNotFoundError:
        pass
    else:
        pytest.fail("This call should fail and raise a FileNotFoundError")

    p = last_dir("a/b/c")
    assert p == "c"
    p = last_dir("d")
    assert p == "d"
    p = last_dir("/")
    assert p == ""

    p = parent_dir("a/b/c/")
    assert p == "a/b/c"
    p = parent_dir("a/b/c")
    assert p == "a/b"
    p = parent_dir("d")
    assert p == ""
    p = parent_dir("/")
    assert p == "/"

    p = root_path("a", "b", "c")
    assert p == "/a/b/c"
    p = root_path()
    assert p == "/"
    p = root_path("a", "b", "/", "c")
    assert p == "/c"

    # FIXME: how to test?
    current_dir()

    # FIXME: how to test?
    script_abspath("test.txt", "a")

    m = module_from_package("a.b.c")
    assert m == "c"
    m = module_from_package("a")
    assert m == "a"
    m = module_from_package("")
    assert m == ""

    p = project_dir("test")
    assert p == "./projects/test"

    # FIXME: how to test?
    # get_api_url(
