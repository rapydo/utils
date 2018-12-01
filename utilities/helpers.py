# -*- coding: utf-8 -*-

import os
import re
import sys
import random
import contextlib
from utilities import PROJECT_DIR
from urllib.parse import urlparse

pathjoin = os.path.join


#######################
# PATH UTILS
def list_path(path):
    return os.listdir(path)


def last_dir(path, level=1):

    suffix = ""
    current_level = level
    path = str(path)
    while current_level > 0:
        if suffix != "":
            suffix = '/' + suffix
        suffix = os.path.basename(path) + suffix
        current_level -= 1
        if current_level > 0:
            path = os.path.dirname(path)

    return suffix


def parent_dir(path):
    return os.path.dirname(path)


#######################
# WITH SUFFIXES
def root_path(*suffixes):
    return pathjoin(os.path.abspath(os.sep), *suffixes)


def script_abspath(file, *suffixes):
    return pathjoin(os.path.dirname(os.path.realpath(file)), *suffixes)


def current_dir(*suffixes):
    return pathjoin(os.curdir, *suffixes)


def current_fullpath(*suffixes):
    return pathjoin(os.getcwd(), *suffixes)


def latest_dir(path):
    return next(reversed(list(os.path.split(path))))


#######################
# RANDOM
def random_name(lenght=10):
    import string

    return ''.join(
        random.choice(
            # string.ascii_uppercase
            string.ascii_lowercase + string.digits
        ) for _ in range(lenght))


def random_element(mylist):
    """ Recover a random element from a list """
    if not isinstance(mylist, list):
        return None
    if len(mylist) < 1:
        return None
    index = random.randint(0, len(mylist) - 1)
    # log.debug("Random index: %s", index)
    return mylist.pop(index)


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


def ask_yes_or_no(question, error='Unknown', print_function=None):

    if print_function is None:
        print_function = print

    answer = 'unknown'
    possible_answers = ['yes', 'y', 'no', 'n']

    while True:
        print_function(question)
        try:
            answer = input('(y/n) ')
        except BaseException as e:
            raise e
        finally:
            if answer == 'unknown' or answer.strip() == '':
                print("\nInterrupted!!\n")
                # log.warning("Interrupted by the user")

        if answer not in possible_answers:
            print("Please answer one of the following: %s" % possible_answers)
        else:
            if answer.strip().startswith('y'):
                break
            else:
                print('USER INTERRUPT:\t' + error)
                sys.exit(1)


@contextlib.contextmanager
def nooutput():
    """ Thanks Alex: https://stackoverflow.com/a/1810086 """
    savestderr = sys.stderr
    savestdout = sys.stdout

    class Devnull(object):

        def write(self, _):
            pass

        def flush(self):
            pass

    sys.stdout = Devnull()
    sys.stderr = Devnull()
    try:
        yield
    finally:
        sys.stdout = savestdout
        sys.stderr = savestderr
