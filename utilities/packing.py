# -*- coding: utf-8 -*-

# BEWARE: to not import this package at startup,
# but only into functions otherwise pip will go crazy
# (we cannot understand why, but it does!)

from utilities.checks import import_exceptions
try:
    from pip.utils import get_installed_distributions
except import_exceptions:
    # from pip 10
    from pip._internal.utils.misc import get_installed_distributions
from sultan.api import Sultan
# from pip import main as pip_exec
from utilities.logs import get_logger

log = get_logger(__name__)


def install(package, editable=False):
    with Sultan.load(sudo=True) as sultan:
        command = 'install --upgrade'
        if editable:
            command += " --editable"
        command += ' %s' % package

        result = sultan.pip3(command).run()

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
