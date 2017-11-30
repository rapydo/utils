# -*- coding: utf-8 -*-

import pytest
import yaml
from utilities.myyaml import load_yaml_file
from utilities.basher import BashCommands


def test_missing_files(capfd):
    # Default is logger=True => print warning
    yaml_file = load_yaml_file("blabla")
    assert yaml_file == {}

    # If logger=False => raise Exception
    try:
        yaml_file = load_yaml_file("blabla", logger=False)
    except AttributeError:
        pass
    else:
        pytest.fail("AttributeError not raised with missing yaml file")

    # Testing optional yaml file
    # Logger=False but skip_error=True -> do nothing
    yaml_file = load_yaml_file("xxyyzz", logger=False, skip_error=True)
    assert yaml_file == {}

    out, err = capfd.readouterr()
    out = out.split("\n")
    err = err.split("\n")

    prefix_msg = "WARNING Failed to read YAML file ["
    suffix_msg = "]: File does not exist"

    f1 = "%s%s%s" % (prefix_msg, "blabla", suffix_msg)
    f2 = "%s%s%s" % (prefix_msg, "xxyyzz", suffix_msg)
    assert f1 in err
    assert f2 not in err


def test_regular_file():

    pass
    # yaml_path = "utilities/projects_defaults.yaml"
    # yaml_file = load_yaml_file(yaml_path, keep_order=True)
    # assert "variables" in yaml_file
    # assert "project" in yaml_file
    # assert "tags" in yaml_file


def test_syntax_errors():

    pass
    # bash = BashCommands()
    # yaml_file = "mytest.yaml"
    # bash.copy("utilities/projects_defaults.yaml", yaml_file)
    # # Introducing a syntax error
    # bash.replace_in_file("project:", " project", yaml_file)
    # try:
    #     load_yaml_file(yaml_file)
    # except yaml.parser.ParserError:
    #     pass
    # else:
    #     pytest.fail("This call should fail and raise a ParserError")
    # bash.remove(yaml_file)
