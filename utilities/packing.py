# -*- coding: utf-8 -*-

from pip.utils import get_installed_distributions
from sultan.api import Sultan
# from pip import main as pip_exec
from utilities.logs import get_logger

log = get_logger(__name__)


def install(package):
    with Sultan.load(sudo=True) as sultan:
        result = sultan.pip3('install --upgrade %s' % package).run()

        for r in result.stdout:
            print(r)

        for r in result.stderr:
            print(r)
        return result.rc == 0
    # pip_exec(['install', '--upgrade', package])


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
