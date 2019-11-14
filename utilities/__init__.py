# -*- coding: utf-8 -*-

import os

__version__ = '1.0.0'
__authors__ = ["Paolo D'Onorio De Meo <p.donorio.demeo@gmail.com>", "Mattia D'Antonio"]

FRAMEWORK_NAME = 'RAPyDo'
PROJECTS_DEFAULTS_FILE = 'projects_defaults'
PROJECT_CONF_FILENAME = 'project_configuration'
PROJECT_DIR = 'projects'
SWAGGER_DIR = 'swagger'
MODELS_DIR = 'models'
CONF_PATH = 'confs'
EXTENDED_PROJECT_DISABLED = "no_extended_project"

GITREPOS_TEAM = FRAMEWORK_NAME.lower()
CONTAINERS_YAML_DIRNAME = CONF_PATH
UTILS_PKGNAME = __package__.split('.')[::-1][0]

BACKEND_DIR = 'backend'  # directory outside docker
MAIN_PACKAGE = 'restapi'
BACKEND_PACKAGE = MAIN_PACKAGE  # package inside rapydo-http
CUSTOM_PACKAGE = os.environ.get('VANILLA_PACKAGE', 'custom')
EXTENDED_PACKAGE = os.environ.get('EXTENDED_PACKAGE', None)
CORE_CONFIG_PATH = os.path.join(BACKEND_PACKAGE, CONF_PATH)
ENDPOINTS_CODE_DIR = 'apis'
