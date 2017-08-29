# -*- coding: utf-8 -*-

# TODO: refactor as a class please

import os
from contextlib import contextmanager
from pathlib import Path
from utilities.logs import get_logger

log = get_logger(__name__)


@contextmanager
def cd(newdir):
    """
    https://stackoverflow.com/a/24176022
    """
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def build(path):
    if not isinstance(path, list):
        if isinstance(path, str):
            path = [path]
        else:
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
        # pathobj.mkdir(exist_ok=force)  # does not work with Python 3.4...
        try:
            pathobj.mkdir()
        except FileExistsError:
            if force:
                pass
            else:
                log.exit("Cannot overwrite existing: %s" % pathobj)
    else:
        raise NotImplementedError("Yet to do!")


def file_exists_and_nonzero(pathobj):
    if pathobj.exists():
        return not pathobj.stat().st_size == 0
    else:
        return False


def existing(path_list, error_msg_base='Failed'):

    filepath = build(path_list)

    if not file_exists_and_nonzero(filepath):
        log.exit(error_msg_base + ": file %s not found" % filepath)
    else:
        log.verbose('"%s" located' % filepath)

    return str(filepath)
