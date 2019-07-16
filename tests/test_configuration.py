# -*- coding: utf-8 -*-

import pytest
from utilities.configuration import read
from utilities.basher import BashCommands


def test():

    project_conf = "projects/template/project_configuration.yaml"
    default_conf = "submodules/rapydo-confs/projects_defaults.yaml"

    # project_configuration is missing
    try:
        read("template")
    except SystemExit:
        pass
    else:
        pytest.fail("SystemExit should be raised because file not exists")

    bash = BashCommands()
    bash.create_directory("projects")
    bash.create_directory("projects/template")
    bash.copy(default_conf, project_conf)

    bash.replace_in_file("name: rapydo", "name: myname", project_conf)

    # project_configuration is ok
    conf = read("template")

    assert "project" in conf
    assert "name" in conf["project"]
    assert conf["project"]["name"] == "myname"

    # project_configuration is missing required info
    bash.replace_in_file("project:", "blabla:", project_conf)
    try:
        conf = read("template")
    except AttributeError:
        pass
    else:
        pytest.fail("This call should fail and raise an AttributeError")

    # bash.remove_directory("projects")
