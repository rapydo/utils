# -*- coding: utf-8 -*-

import os
import re
from rapydo.utils import PROJECT_DIR
from urllib.parse import urlparse


#######################
# PATH UTILS
def list_path(path):
    return os.listdir(path)


def last_dir(path):
    return os.path.basename(path)


def parent_dir(path):
    return os.path.dirname(path)


#######################
# WITH SUFFIXES
def root_path(*suffixes):
    return os.path.join(os.path.abspath(os.sep), *suffixes)


def script_abspath(file, *suffixes):
    return os.path.join(os.path.dirname(os.path.realpath(file)), *suffixes)


def current_dir(*suffixes):
    return os.path.join(os.curdir, *suffixes)


#######################
# OTHERS
def module_from_package(package):
    return package.split('.')[::-1][0]


def project_dir(project, *suffixes):
    return current_dir(PROJECT_DIR, project, *suffixes)


def get_api_url(request_object, production=False):
    """ Get api URL and PORT

    Usefull to handle https and similar
    unfiltering what is changed from nginx and container network configuration

    Warning: it works only if called inside a Flask endpoint
    """

    api_url = request_object.url_root

    if production:
        parsed = urlparse(api_url)
        if parsed.port is not None and parsed.port == 443:
            removed_port = re.sub(r':[\d]+$', '', parsed.netloc)
            api_url = parsed._replace(
                scheme="https", netloc=removed_port
            ).geturl()

    return api_url
