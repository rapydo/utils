# -*- coding: utf-8 -*-

# TODO: refactor as a class please

from pathlib import Path
from utilities.logs import get_logger

log = get_logger(__name__)


def build(path):
    if not isinstance(path, list):
        path = list(path)
    p = Path(*path)
    return p


def join(*paths):
    return build(paths)


def home(relative_path=None):
    if relative_path is None:
        return Path.home()
    else:
        if relative_path.startswith('/'):
            log.exit(
                "Requested abspath '%s' in relative context" % relative_path)
        return build('~/' + relative_path).expanduser()


def current():
    return Path.cwd()


def create(pathobj, directory=False, force=False):
    if directory:
        pathobj.mkdir(exist_ok=force)
    else:
        raise NotImplementedError("Yet to do!")
