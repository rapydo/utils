# -*- coding: utf-8 -*-

import os
from utilities import PROJECT_CONF_FILENAME, PROJECTS_DEFAULTS_FILE
from utilities.myyaml import load_yaml_file
from utilities.logs import get_logger

log = get_logger(__name__)


def load_project_configuration(path, file=None, do_exit=True):

    if file is None:
        file = PROJECT_CONF_FILENAME

    args = {
        'path': path,
        'skip_error': False,
        'logger': False,
        'file': file,
        'keep_order': True
    }
    try:
        log.checked("Found '%s/%s' configuration", path, file)
        return load_yaml_file(**args)
    except AttributeError as e:
        if do_exit:
            log.exit(e)
        else:
            raise AttributeError(e)


def read(default_file_path, base_project_path,
         projects_path, submodules_path,
         from_configuration_prefix="",
         is_template=False,
         do_exit=True,
         ):
    """
    Read default configuration
    """

    custom_configuration = load_project_configuration(
        base_project_path, file=PROJECT_CONF_FILENAME, do_exit=do_exit)

    # Verify custom project configuration
    project = custom_configuration.get('project')
    if project is None:
        raise AttributeError("Missing project configuration")

    if not is_template:

        # Check if these three variables were changed from the initial template
        checks = {
            'title': 'My project',
            'description': 'Title of my project',
            'name': 'rapydo'
        }
        for key, value in checks.items():
            if project.get(key, '') == value:

                log.critical_exit(
                    "Project not configured, mising key '%s' in file %s/%s.yaml",
                    key, base_project_path, PROJECT_CONF_FILENAME
                )

    base_configuration = load_project_configuration(
        default_file_path, file=PROJECTS_DEFAULTS_FILE, do_exit=do_exit)

    from_project = project.get('extends')
    if from_project is None:
        # Mix default and custom configuration
        return mix(base_configuration, custom_configuration), None, None

    extends_from = project.get('extends-from', 'projects')

    if extends_from == "submodules":
        from_path = os.path.join(submodules_path, from_project)
    else:
        from_path = os.path.join(projects_path, from_project)

    if not os.path.exists(from_path):
        log.critical_exit("From project not found: %s", from_path)

    # on backend is mounted with `from_` prefix
    from_file = "%s%s" % (from_configuration_prefix, PROJECT_CONF_FILENAME)
    from_configuration = load_project_configuration(
        from_path, file=from_file, do_exit=do_exit)

    m1 = mix(base_configuration, from_configuration)
    return mix(m1, custom_configuration), from_project, from_path


def mix(base, custom):

    for key, elements in custom.items():

        if key not in base:
            # log.info("Adding %s to configuration" % key)
            base[key] = custom[key]
            continue

        if isinstance(elements, dict):
            mix(base[key], custom[key])

        elif isinstance(elements, list):
            for e in elements:
                base[key].append(e)
        else:
            # log.info("Replacing default %s in configuration" % key)
            base[key] = elements

    return base
