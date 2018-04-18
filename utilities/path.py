# -*- coding: utf-8 -*-

"""
TODO: apply the / magic of pathlib
src: http://j.mp/2nwz908
"""

import os
from contextlib import contextmanager
from pathlib import Path, PurePath
from utilities.logs import get_logger

log = get_logger(__name__)
COMPRESSION_FORMAT = 'zip'


def root():
    return os.path.abspath(os.sep)


@contextmanager
def cd(newdir):
    """
    https://stackoverflow.com/a/24176022
    """
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(str(newdir)))
    try:
        yield
    finally:
        os.chdir(prevdir)


def build(path=None):

    # no path would just mean the FS root directory
    if path is None:
        path = root()

    if not isinstance(path, list):
        if isinstance(path, str) or isinstance(path, Path):
            path = [path]
        else:
            path = list(path)

    p = Path(*path)
    return p


def join(*paths, return_str=False):
    path = build(paths)
    if return_str:
        path = str(path)
    return path


def home(relative_path=None):
    if relative_path is None:
        return Path.home()
    else:
        if relative_path.startswith(os.sep):
            log.exit(
                "Requested abspath '%s' in relative context" % relative_path)
        return build('~' + os.sep + relative_path).expanduser()


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


def file_exists_and_nonzero(pathobj, accept_link=False):

    if pathobj.exists():
        iostats = pathobj.stat()
        # log.pp(iostats)
        return not iostats.st_size == 0
    else:
        if accept_link:
            if os.path.islink(pathobj):
                return True
        return False


def existing(path_list, error_msg_base='Failed', do_exit=True):

    filepath = build(path_list)

    if not file_exists_and_nonzero(filepath):
        if do_exit:
            log.exit(error_msg_base + ": file %s not found" % filepath)
        else:
            return False
    else:
        log.verbose('"%s" located' % filepath)
        if not do_exit:
            return True

    return str(filepath)


def parts(my_path):
    return PurePath(my_path).parts


def last_part(my_path):
    return os.path.basename(my_path)


def dir_name(my_path):
    return os.path.dirname(my_path)


def append_compress_extension(base_name):
    return '%s.%s' % (base_name, COMPRESSION_FORMAT)


def compress(dir_path, zip_file_path):
    import shutil
    base_name = str(zip_file_path).replace('.' + COMPRESSION_FORMAT, '')
    shutil.make_archive(
        base_name=base_name, format=COMPRESSION_FORMAT, root_dir=dir_path)
