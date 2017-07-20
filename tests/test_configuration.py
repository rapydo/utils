
import pytest
from utilities.configuration import read
from utilities.basher import BashCommands


def replace_in_file(bash, target, destination, file):
    params = [
        "-i",
        "s/%s/%s/g" % (target, destination),
        file
    ]
    bash.execute_command("sed", params)


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

    replace_in_file(bash, "My project", "My title", project_conf)
    replace_in_file(bash, "name: rapydo", "name: myname", project_conf)
    replace_in_file(bash, "Title of my project", "My title", project_conf)
    replace_in_file(bash, "tags:", "mycustomvar:", project_conf)

    conf = read("template")

    assert "project" in conf
    assert "mycustomvar" in conf
    assert "name" in conf["project"]
    assert conf["project"]["name"] == "myname"

    replace_in_file(bash, "project:", "blabla:", project_conf)
    try:
        conf = read("template")
    except AttributeError:
        pass
    else:
        pytest.fail("This call should fail and raise an AttributeError")

    bash.remove_directory("projects")
