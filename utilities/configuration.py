# -*- coding: utf-8 -*-

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


def read(base_path, project_path=None, is_template=False, do_exit=True):
    """
    Read default configuration
    """

    base_configuration = load_project_configuration(
        base_path, file=PROJECTS_DEFAULTS_FILE, do_exit=do_exit)

    if project_path is None:
        return base_configuration

    custom_configuration = load_project_configuration(
        project_path, file=PROJECT_CONF_FILENAME, do_exit=do_exit)

    # Verify custom project configuration
    prj = custom_configuration.get('project')
    if prj is None:
        raise AttributeError("Missing project configuration")

    if not is_template:

        # Check if these three variables were changed from the initial template
        checks = {
            'title': 'My project',
            'description': 'Title of my project',
            'name': 'rapydo'
        }
        for key, value in checks.items():
            if prj.get(key, '') == value:

                log.critical_exit(
                    "Project not configured, mising key '%s' in file %s/%s.yaml",
                    key, project_path, PROJECT_CONF_FILENAME
                )

    # Mix default and custom configuration
    return mix(base_configuration, custom_configuration)


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
