# -*- coding: utf-8 -*-

import os

__version__ = '0.6.2'
__authors__ = [
    "Paolo D'Onorio De Meo <p.donorio.demeo@gmail.com>",
    "Mattia D'Antonio",
]

###############
FRAMEWORK_NAME = 'RAPyDo'

# TOOLS = [
#     'utils',
#     'core',
#     'frontend',
#     'do',
#     'develop',
#     'build-templates',
#     'http-api',
# ]
# ORDER: utils > core > do > develop > builds > http-api > frontend

###############
PROJECTS_DEFAULTS_FILE = 'projects_defaults'
PROJECT_CONF_FILENAME = 'project_configuration'
PROJECT_DIR = 'projects'
DEFAULT_TEMPLATE_PROJECT = 'template'
SWAGGER_DIR = 'swagger'
MODELS_DIR = 'models'
SWAGGER_MODELS_FILE = 'models'
CONF_PATH = 'confs'

GITREPOS_TEAM = FRAMEWORK_NAME.lower()
CONTAINERS_YAML_DIRNAME = CONF_PATH
UTILS_PKGNAME = __package__.split('.')[::-1][0]

BACKEND_DIR = 'backend'  # directory outside docker
MAIN_PACKAGE = 'restapi'
BACKEND_PACKAGE = MAIN_PACKAGE  # package inside rapydo-http
CUSTOM_PACKAGE = os.environ.get('VANILLA_PACKAGE', 'custom')
CORE_CONFIG_PATH = os.path.join(BACKEND_PACKAGE, CONF_PATH)
ENDPOINTS_CODE_DIR = 'apis'
