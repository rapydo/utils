
import pytest
import yaml
from utilities.myyaml import load_yaml_file
from utilities.basher import BashCommands


def test():
    yaml_path = "utilities/projects_defaults.yaml"
    yaml_file = load_yaml_file("blabla")
    assert yaml_file == {}
    try:
        yaml_file = load_yaml_file("blabla", logger=False)
    except AttributeError:
        pass
    else:
        pytest.fail("AttributeError not raised with missing yaml file")
    yaml_file = load_yaml_file(yaml_path, keep_order=True)

    assert "variables" in yaml_file
    assert "project" in yaml_file
    assert "tags" in yaml_file

    bash = BashCommands()
    yaml_file = "mytest.yaml"
    bash.copy("utilities/projects_defaults.yaml", yaml_file)
    # Introducing a syntax error
    bash.replace_in_file("project:", " project", yaml_file)
    try:
        load_yaml_file(yaml_file)
    except yaml.parser.ParserError:
        pass
    else:
        pytest.fail("This call should fail and raise a ParserError")
    bash.remove(yaml_file)
