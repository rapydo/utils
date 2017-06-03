# -*- coding: utf-8 -*-

from pip.utils import get_installed_distributions
from pip import main as pip_exec


def install(package):
    pip_exec(['install', package])


def list_all():
    return get_installed_distributions(local_only=True, user_only=False)


def check_version(package_name):
    for pkg in list_all():
        if pkg.get('_key') == package_name:
            return pkg.get('_version')

    return None
