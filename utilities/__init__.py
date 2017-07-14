# -*- coding: utf-8 -*-

__version__ = '0.5.0'
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

MAIN_PACKAGE = FRAMEWORK_NAME.lower()
CONTAINERS_YAML_DIRNAME = CONF_PATH
UTILS_PKGNAME = __package__.split('.')[::-1][0]

classifiers = [
    'Programming Language :: Python',
    'Intended Audience :: Developers',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]
