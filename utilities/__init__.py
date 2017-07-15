# -*- coding: utf-8 -*-

import os

__version__ = '0.5.1'
__authors__ = [
    "Paolo D'Onorio De Meo <p.donorio.demeo@gmail.com>",
    "Mattia D'Antonio",
]

FRAMEWORK_NAME = 'RAPyDo'

DEFAULT_FILENAME = 'projects_defaults'
PROJECT_CONF_FILENAME = 'project_configuration'
PROJECT_DIR = 'projects'
DEFAULT_TEMPLATE_PROJECT = 'template'
SWAGGER_DIR = 'swagger'
SWAGGER_MODELS_FILE = 'params_models'
CONF_PATH = 'confs'

# MAIN_PACKAGE = FRAMEWORK_NAME.lower()
CONTAINERS_YAML_DIRNAME = CONF_PATH
UTILS_PKGNAME = __package__.split('.')[::-1][0]

MAIN_PACKAGE = 'restapi'
BACKEND_PACKAGE = MAIN_PACKAGE  # package inside rapydo-http
CUSTOM_PACKAGE = os.environ.get('VANILLA_PACKAGE', 'custom')
CORE_CONFIG_PATH = os.path.join(BACKEND_PACKAGE, 'confs')
