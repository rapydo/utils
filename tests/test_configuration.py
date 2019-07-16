# -*- coding: utf-8 -*-

import pytest
from utilities.configuration import read
from utilities import helpers
from utilities import PROJECT_DIR
from utilities.basher import BashCommands


def test():

    SUBMODULES_DIR = 'submodules'
    DEFAULTS_PATH = 'rapydo-confs'
    project = "template"
    project_file_path = helpers.project_dir(project)
    project_conf = "%s/project_configuration.yaml" % project_file_path
    default_conf = "%s/projects_defaults.yaml" % DEFAULTS_PATH

    # project_configuration is missing
    try:
        read(DEFAULTS_PATH, project_file_path, PROJECT_DIR, SUBMODULES_DIR)
    except SystemExit:
        pass
    else:
        pytest.fail("SystemExit should be raised because file not exists")

    bash = BashCommands()
    bash.create_directory("projects")
    bash.create_directory("projects/template")
    bash.copy(default_conf, project_conf)

    bash.replace_in_file(
        "description: No description yet",
        "description: My description",
        project_conf
    )

    # project_configuration is ok
    conf = read(DEFAULTS_PATH, project_file_path, PROJECT_DIR, SUBMODULES_DIR)

    assert "project" in conf
    assert "description" in conf["project"]
    assert conf["project"]["description"] == "My description"

    # project_configuration is missing required info
    bash.replace_in_file("project:", "blabla:", project_conf)
    try:
        conf = read("template")
    except AttributeError:
        pass
    else:
        pytest.fail("This call should fail and raise an AttributeError")

    # bash.remove_directory("projects")
