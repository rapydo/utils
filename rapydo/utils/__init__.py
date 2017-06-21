# -*- coding: utf-8 -*-

__version__ = '0.4.5'

FRAMEWORK_NAME = 'RAPyDo'

DEFAULT_FILENAME = 'projects_defaults'
PROJECT_CONF_FILENAME = 'project_configuration'
PROJECT_DIR = 'projects'
DEFAULT_TEMPLATE_PROJECT = 'template'
SWAGGER_DIR = 'swagger'
SWAGGER_MODELS_FILE = 'params_models'
CONF_PATH = 'confs'

MAIN_PACKAGE = FRAMEWORK_NAME.lower()
CONTAINERS_YAML_DIRNAME = CONF_PATH
UTILS_PKGNAME = __package__.split('.')[::-1][0]
