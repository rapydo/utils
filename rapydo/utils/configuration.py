# -*- coding: utf-8 -*-

import os
from rapydo.utils import PROJECT_CONF_FILENAME, DEFAULT_FILENAME
from rapydo.utils import helpers
from rapydo.utils.myyaml import load_yaml_file, YAML_EXT
from rapydo.utils.logs import get_logger

log = get_logger(__name__)

SCRIPT_PATH = helpers.script_abspath(__file__)
DEFAULT_CONFIG_FILEPATH = os.path.join(
    SCRIPT_PATH,
    '%s.%s' % (DEFAULT_FILENAME, YAML_EXT)
)


def read(project, is_template=False):
    """
    Read default configuration
    """

    project_configuration_files = \
        [
            # DEFAULT
            {
                'path': SCRIPT_PATH,
                'skip_error': False,
                'logger': False,
                'file': DEFAULT_FILENAME
            },
            # CUSTOM FROM THE USER
            {
                'path': helpers.project_dir(project),
                'skip_error': False,
                'logger': False,
                'file': PROJECT_CONF_FILENAME
            },
        ]

    confs = {}

    for args in project_configuration_files:
        try:
            args['keep_order'] = True
            f = args['file']
            confs[f] = load_yaml_file(**args)
            log.debug("(CHECKED) found '%s' rapydo configuration" % f)
        except AttributeError as e:
            log.critical_exit(e)

    # Recover the two options
    base_configuration = confs.get(DEFAULT_FILENAME)
    custom_configuration = confs.get(PROJECT_CONF_FILENAME, {})

    # Verify custom project configuration
    prj = custom_configuration.get('project')
    if prj is None:
        raise AttributeError("Missing project configuration")
    elif not is_template:
        check1 = prj.get('title') == 'My project'
        check2 = prj.get('description') == 'Title of my project'
        check3 = prj.get('name') == 'rapydo'
        if check1 or check2 or check3:
            filepath = load_yaml_file(return_path=True, **args)
            log.critical_exit(
                "\n\nIt seems like your project is not yet configured...\n" +
                "Please edit file %s" % filepath
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
        else:
            # log.info("Replacing default %s in configuration" % key)
            base[key] = elements

    return base
