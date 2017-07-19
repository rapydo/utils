
import pytest
from utilities.configuration import read
from utilities.basher import BashCommands


def test():

    project_conf = "projects/template/project_configuration.yaml" 
    bash = BashCommands()
    bash.create_directory("projects")
    bash.create_directory("projects/template")
    params = [
        "utilities/projects_defaults.yaml",
        project_conf
    ]
    bash.execute_command("cp", params)

    try:
        read("template")
    except SystemExit:
        pass
    else:
        pytest.fail("A SystemExit should be raised due to use of default conf")

    params = [
        "-i",
        "s/My project/My custom title/g",
        project_conf
    ]
    bash.execute_command("sed", params)

    params = [
        "-i",
        "s/name: rapydo/name: myname/g",
        project_conf
    ]
    bash.execute_command("sed", params)

    params = [
        "-i",
        "s/Title of my project/My custom title/g",
        project_conf
    ]
    bash.execute_command("sed", params)
    conf = read("template")

    assert "project" in conf
    assert "name" in conf["project"]
    assert conf["project"]["name"] == "myname"

    bash.remove_directory("projects")
