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
        'keep_order': True,
    }
    try:
        log.checked("Found '%s/%s' configuration", path, file)
        return load_yaml_file(**args)
    except AttributeError as e:
        if do_exit:
            log.exit(e)
        else:
            raise AttributeError(e)


def read(
    default_file_path,
    base_project_path,
    projects_path,
    submodules_path,
    from_container=False,
    read_extended=True,
    do_exit=True,
):
    """
    Read default configuration
    """

    custom_configuration = load_project_configuration(
        base_project_path, file=PROJECT_CONF_FILENAME, do_exit=do_exit
    )

    # Verify custom project configuration
    project = custom_configuration.get('project')
    if project is None:
        raise AttributeError("Missing project configuration")

    variables = ['title', 'description', 'version', 'rapydo']

    for key in variables:
        if project.get(key) is None:

            log.critical_exit(
                "Project not configured, missing key '%s' in file %s/%s.yaml",
                key,
                base_project_path,
                PROJECT_CONF_FILENAME,
            )

    if default_file_path is None:
        base_configuration = {}
    else:
        base_configuration = load_project_configuration(
            default_file_path, file=PROJECTS_DEFAULTS_FILE, do_exit=do_exit
        )

    if read_extended:
        extended_project = project.get('extends')
    else:
        extended_project = None
    if extended_project is None:
        # Mix default and custom configuration
        return mix(base_configuration, custom_configuration), None, None

    extends_from = project.get('extends-from', 'projects')

    if extends_from == "projects":
        extend_path = projects_path
    elif extends_from.startswith("submodules/"):
        repository_name = (extends_from.split("/")[1]).strip()
        if repository_name == '':
            log.exit('Invalid repository name in extends-from, name is empty')

        if from_container:
            extend_path = submodules_path
        else:
            extend_path = os.path.join(submodules_path, repository_name, projects_path)
    else:
        suggest = "Expected values: 'projects' or 'submodules/${REPOSITORY_NAME}'"
        log.exit("Invalid extends-from parameter: %s.\n%s", extends_from, suggest)

    # in container the file is mounted in the confs folder
    # otherwise will be in projects/projectname or submodules/projectname
    if not from_container:
        extend_path = os.path.join(extend_path, extended_project)

    if not os.path.exists(extend_path):
        log.critical_exit("From project not found: %s", extend_path)

    # on backend is mounted with `extended_` prefix
    if from_container:
        extend_file = "extended_%s" % (PROJECT_CONF_FILENAME)
    else:
        extend_file = PROJECT_CONF_FILENAME
    extended_configuration = load_project_configuration(
        extend_path, file=extend_file, do_exit=do_exit
    )

    m1 = mix(base_configuration, extended_configuration)
    return mix(m1, custom_configuration), extended_project, extend_path


def mix(base, custom):
    if base is None:
        base = {}

    for key, elements in custom.items():

        if key not in base:
            # log.info("Adding %s to configuration" % key)
            base[key] = custom[key]
            continue

        if elements is None:
            if isinstance(base[key], dict):
                log.warning("Cannot replace %s with empty list", key)
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
