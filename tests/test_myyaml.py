
from utilities.myyaml import load_yaml_file


def test():
    yaml_path = "../utilities/projects_defaults.yaml"
    load_yaml_file(yaml_path)
    yaml = load_yaml_file(yaml_path, keep_order=True)

    assert "variables" in yaml
    assert "project" in yaml
    assert "tags" in yaml
