# -*- coding: utf-8 -*-

# import os
from utilities import PROJECT_CONF_FILENAME, PROJECTS_DEFAULTS_FILE
from utilities.myyaml import load_yaml_file
from utilities.logs import get_logger

log = get_logger(__name__)

# SCRIPT_PATH = helpers.script_abspath(__file__)


def load_project_configuration(project_path):
    args = {
        'path': project_path,
        'skip_error': False,
        'logger': False,
        'file': PROJECT_CONF_FILENAME,
        'keep_order': True
    }
    return load_yaml_file(**args)


def read(base_path, project_path=None, is_template=False, do_exit=True):
    """
    Read default configuration
    """

    project_configuration_files = [
        # DEFAULT
        {
            # 'path': SCRIPT_PATH,
            'path': base_path,
            'skip_error': False,
            'logger': False,
            'file': PROJECTS_DEFAULTS_FILE
        }
    ]

    if project_path is not None:
        project_configuration_files.append(
            # CUSTOM FROM THE USER
            {
                'path': project_path,
                'skip_error': False,
                'logger': False,
                'file': PROJECT_CONF_FILENAME
            }
        )

    confs = {}

    for args in project_configuration_files:
        try:
            args['keep_order'] = True
            f = args['file']
            confs[f] = load_yaml_file(**args)
            log.checked("Found '%s' rapydo configuration" % f)
        except AttributeError as e:
            if do_exit:
                log.exit(e)
            else:
                raise AttributeError(e)

    # Recover the two options
    base_configuration = confs.get(PROJECTS_DEFAULTS_FILE)
    if project_path is None:
        return base_configuration
    custom_configuration = confs.get(PROJECT_CONF_FILENAME, {})

    # Verify custom project configuration
    prj = custom_configuration.get('project')
    if prj is None:
        raise AttributeError("Missing project configuration")
    elif not is_template:

        # Check if these three variables were changed from the initial template
        checks = {
            'title': 'My project',
            'description': 'Title of my project',
            'name': 'rapydo'
        }
        for key, value in checks.items():
            if prj.get(key, '') == value:

                # get file name with the load file utility
                args = {}
                kwargs = project_configuration_files.pop()
                filepath = load_yaml_file(
                    *args, return_path=True, **kwargs)

                log.critical_exit(
                    "\n\nYour project is not yet configured:\n" +
                    "Please edit key '%s' in file %s" % (key, filepath)
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
