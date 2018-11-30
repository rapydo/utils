# -*- coding: utf-8 -*-

import os
import yaml
from collections import OrderedDict
# from functools import lru_cache

YAML_EXT = 'yaml'
SHORT_YAML_EXT = 'yml'

# Test the library as soon as possible
yaml.dump({})


#####################
class OrderedLoader(yaml.SafeLoader):
    """
    A 'workaround' good enough for ordered loading of dictionaries

    https://stackoverflow.com/a/21912744

    NOTE: This was created to skip dependencies.
    Otherwise this option could be considered:
    https://pypi.python.org/pypi/ruamel.yaml
    """
    pass


def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


def regular_load(stream, loader=yaml.loader.Loader):
    # LOAD fails if more than one document is there
    # return yaml.load(fh)

    # LOAD ALL gets more than one document inside the file
    # gen = yaml.load_all(fh)
    return yaml.load_all(stream, loader)


def ordered_load(stream):

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    # return yaml.load(stream, OrderedLoader)
    return regular_load(stream, OrderedLoader)


#####################
def get_yaml_path(path, filename, extension):
    if path is None:
        filepath = filename
    else:
        if extension is not None:
            filename += '.' + extension
        filepath = os.path.join(path, filename)

    return filepath


def get_loader(fh, keep_order):
    # LOAD ordered
    if keep_order:
        return ordered_load(fh)
    else:
        return regular_load(fh)


# @lru_cache()
def load_yaml_file(file, path=None,
                   get_all=False, skip_error=False,
                   extension=YAML_EXT, return_path=False,
                   logger=True, keep_order=False):
    """
    Import any data from a YAML file.

    NOTE: the logger problem

    Since YAML are important files for configuration in our case,
    we may be in the situation of not having the loggers yet,
    since the configuration in itself is needed to configure the logger.

    In that case we have logger=False and a silenced read.
    """

    if logger:
        from utilities.logs import get_logger
        log = get_logger(__name__)

    filepath = get_yaml_path(path, file, extension)

    if not return_path and logger:
        log.very_verbose("Reading file %s" % filepath)

    # load from this file
    error = None
    if not os.path.exists(filepath):
        error = 'File does not exist'
    else:
        if return_path:
            return filepath

        with open(filepath) as fh:
            try:
                loader = get_loader(fh, keep_order)
            except Exception as e:
                error = e
            else:
                docs = list(loader)
                if get_all:
                    return docs

                if len(docs) > 0:
                    return docs[0]

                message = "YAML file is empty: %s" % filepath
                if logger:
                    log.exit(message)
                else:
                    raise AttributeError(message)

    # # IF dealing with a strange exception string (escaped)
    # import codecs
    # mystring, _ = codecs.getdecoder("unicode_escape")(str(error))
    # message = "Failed to read YAML file [%s]: %s" % (filepath, mystring)

    message = "Failed to read YAML file [%s]: %s" % (filepath, error)
    if logger:
        log.warning(message)
    elif not skip_error:
        raise AttributeError(message)
    # else:
    #     pass
    return {}
