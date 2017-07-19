
import pytest
from utilities.myyaml import load_yaml_file


def test():
    yaml_path = "utilities/projects_defaults.yaml"
    yaml = load_yaml_file("blabla")
    assert yaml == {}
    try:
        yaml = load_yaml_file("blabla", logger=False)
    except AttributeError:
        pass
    else:
        pytest.fail("AttributeError not raised with missing yaml file")
    yaml = load_yaml_file(yaml_path, keep_order=True)

    assert "variables" in yaml
    assert "project" in yaml
    assert "tags" in yaml
