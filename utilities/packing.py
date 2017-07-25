# -*- coding: utf-8 -*-

from pip.utils import get_installed_distributions
from pip import main as pip_exec


def install(package):
    pip_exec(['install', package])


def list_all():
    return get_installed_distributions(local_only=True, user_only=False)


def check_version(package_name):
    for pkg in list_all():
        # if pkg.get('_key') == package_name:
        if pkg._key == package_name:  # pylint:disable=protected-access
            # return pkg.get('_version')
            try:
                return pkg._version  # pylint:disable=protected-access
            except AttributeError:
                # fix for python 3.4
                return pkg.__dict__

    return None
