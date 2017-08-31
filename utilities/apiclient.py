# -*- coding: utf-8 -*-

"""
Helpers functions
to create a client based on Python against our HTTP API
"""

import os
import sys
from utilities.logs import get_logger, logging, set_global_log_level

LOGIN_ENDPOINT = '/auth/b2safeproxy'
BASIC_ENDPOINT = '/api/registered'
ADVANCEND_ENDPOINT = '/api/pids'

log = get_logger(__name__)


def setup_logger(name, level_name):

    log_level = getattr(logging, level_name.upper())
    set_global_log_level(package=__package__, app_level=log_level)
    return get_logger(name)


def parse_api_output(req):

    content = None
    failed = False
    output_key = 'Response'
    output_content = 'data'
    output_errors = 'errors'

    response = req.json()

    if req.status_code > 299:
        log.critical("API request failed (or not completed)")
        failed = True

    # log.pp(response)  # DEBUG
    if output_key in response:
        output = response[output_key]
        errors = output.get(output_errors, [])
        if errors is not None and len(errors) > 0:
            for error in errors:
                log.error(error)
        content = output.get(output_content)

    if failed:
        log.exit()
    else:
        return content


def call(uri,
         endpoint=None, method='get', payload=None, token=None, file=None):
    """
    Helper function based on 'requests' to easily call our HTTP API in Python
    """

    if endpoint is None:
        endpoint = '/api/status'

    headers = {}
    if token is not None:
        headers['Authorization'] = "Bearer %s" % token

    method = method.lower()
    import requests
    requests_callable = getattr(requests, method)

    if method == 'post':
        import json
        payload = json.dumps(payload)

    log.very_verbose('Calling %s on %s' % (method, endpoint))
    arguments = {
        'url': uri + endpoint,
        'headers': headers,
        'timeout': 10,
    }

    if method == 'get':
        arguments['params'] = payload
    else:
        arguments['data'] = payload

    if file is not None:
        if method != 'put':
            log.exit("Cannot upload a file with method '%s'" % method)
        else:
            try:
                fh = open(file, 'rb')  # , encoding='utf-8'
            except Exception as e:
                raise e
            else:
                name = os.path.basename(file)
                arguments['files'] = {'file': (name, fh)}

        # sending a file
        headers['content-type'] = 'application/octet-stream'
    else:
        # sending normal json/dictionaries data
        headers['content-type'] = 'application/json'

    # call the api
    try:
        request = requests_callable(**arguments)
    except requests.exceptions.ConnectionError as e:
        log.exit("Connection failed:\n%s" % e)
    else:
        log.very_verbose("URL: %s" % request.url)

    out = parse_api_output(request)
    log.verbose("HTTP-API CALL[%s]: %s" % (method.upper(), out))

    return out


def login(uri, username, password, endpoint=None):
    if endpoint is None:
        endpoint = LOGIN_ENDPOINT
    out = call(
        uri, method='post', endpoint=endpoint,
        payload={'username': username, 'password': password}
    )
    log.debug("Current iRODS user: %s" % out.get('b2safe_user'))
    return out.get('token'), out.get('b2safe_home')


def folder_content(folder_path):
    if not os.path.exists(folder_path):
        log.exit("%s does not exist" % folder_path)

    import glob
    log.debug("Looking for directory '%s'" % folder_path)
    files = glob.glob(os.path.join(folder_path, "*"))
    if len(files) < 1:
        log.exit("%s does not contain any file" % folder_path)

    return files


def parse_irods_listing(response, directory):
    to_print = ''
    home_content = []
    for element in response:
        name, obj = element.popitem()
        home_content.append(name)
        metadata = obj.get('metadata', {})
        objtype = metadata.get('object_type')
        to_print += "\n%s [%s]" % (name, objtype)

    if len(home_content) > 0:
        log.info("Directory %s current content: %s\n" % (directory, to_print))
    return home_content
