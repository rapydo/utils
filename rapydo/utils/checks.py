# -*- coding: utf-8 -*-

"""
Pythonic checks on the current system
"""

# from rapydo.utils.logs import get_logger

# log = get_logger(__name__)


# which version of python is this?
# Retrocompatibility for Python < 3.6
try:
    import_exceptions = (ModuleNotFoundError, ImportError)
except NameError:
    import_exceptions = ImportError

DEFAULT_BIN_OPTION = '--version'


def check_executable(executable, option=DEFAULT_BIN_OPTION, log=None):

    from subprocess import check_output
    try:
        stdout = check_output([executable, option])
        output = stdout.decode()
    except OSError:
        return None
    else:
        if option == DEFAULT_BIN_OPTION:
            try:
                # try splitting on coma and/or parenthesis
                # then last element on spaces
                output = output \
                    .split('(')[0].split(',')[0] \
                    .split()[::-1][0]
            except BaseException:
                pass
        return output


def import_package(package_name):

    from importlib import import_module
    try:
        package = import_module(package_name)
    except import_exceptions as e:
        return None
    else:
        return package


def check_package(package_name):
    package = import_package(package_name)
    if package is not None:
        return package.__version__
    else:
        return None


def check_internet(test_site='https://www.google.com'):

    import requests
    try:
        requests.get(test_site)
    except requests.ConnectionError:
        return False
    else:
        return True
