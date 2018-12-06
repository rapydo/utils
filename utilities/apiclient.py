# -*- coding: utf-8 -*-

"""
Helpers functions
to create a client based on Python against our HTTP API
"""

import os
import io
from utilities.logs import \
    get_logger, logging, set_global_log_level, DEFAULT_LOGLEVEL_NAME

LOGIN_ENDPOINT = '/auth/b2safeproxy'
BASIC_ENDPOINT = '/api/registered'
ADVANCEND_ENDPOINT = '/api/pids'

log = get_logger(__name__)

try:
    import requests
except ImportError as e:
    log.exit("\nThis module requires an extra package:\n%s", e)


def setup_logger(name, level_name):

    log_level = getattr(logging, level_name.upper())
    set_global_log_level(package=name, app_level=log_level)
    # log.critical("TRAVIS: %s, %s", name, log_level)
    return get_logger(name)


def check_cli_arg(arg='help', reverse=False, do_exit=False, code=0, get=False):
    import sys
    arg_prefix = '--'
    real_arg = arg_prefix + arg
    check = real_arg in sys.argv

    if reverse:
        check = not check
    elif get:
        if check:
            is_next = False
            for current_arg in sys.argv:
                if is_next:
                    return current_arg
                elif real_arg == current_arg:
                    is_next = True
                # print(current_arg)
        return DEFAULT_LOGLEVEL_NAME

    if check and do_exit:
        sys.exit(code)
    return check


def parse_api_output(req):

    content = None
    failed = False
    output_key = 'Response'
    output_content = 'data'
    output_errors = 'errors'

    response = req.json()

    if req.status_code > 299:
        log.pp(req)
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
         endpoint=None, method='get', payload=None, headers=None,
         token=None, file=None, filecontent=None, filename=None,
         timeout=10, exit_on_fail=True):
    """
    Helper function based on 'requests' to easily call our HTTP API in Python
    """

    if endpoint is None:
        endpoint = '/api/status'

    if headers is None:
        headers = {}
    if token is not None:
        headers['Authorization'] = "Bearer %s" % token

    method = method.lower()
    requests_callable = getattr(requests, method)

    if method in ['post', 'patch', 'put', 'delete']:
        if method != 'put' or file is not None or filecontent is not None:
            import json
            payload = json.dumps(payload)

    log.very_verbose('Calling %s on %s', method, endpoint)
    arguments = {
        'url': uri + endpoint,
        'headers': headers,
        'timeout': timeout,
    }

    if method in ['get']:
        arguments['params'] = payload
    else:
        arguments['data'] = payload

    if file is not None or filecontent is not None:
        if method != 'put':
            log.exit("Cannot upload file in RAPyDo with method '%s'", method)

        # headers['content-type'] = 'application/octet-stream'
        # headers['content-type'] = 'multipart/form-data'
    else:
        # sending normal json/dictionaries data
        if 'Content-Type' not in headers:
            headers['content-type'] = 'application/json'

    # call the api
    try:

        if file is not None:
            # Streaming a file
            with open(file, 'rb') as f:
                arguments['files'] = {'file': f}  # automatically compute name
                # name = os.path.basename(file)
                # arguments['files'] = {'file': (name, f)}

        elif filecontent is not None:
            # Streaming a file
            arguments['data'] = dict(file=(io.BytesIO(filecontent), filename))

        # Skipping ssl verification
        # arguments['verify'] = False

        request = requests_callable(**arguments)

    except requests.exceptions.ConnectionError as e:
        if exit_on_fail:
            log.exit("Connection failed:\n%s", e)
        else:
            return None
    else:
        log.very_verbose("URL: %s", request.url)

    out = parse_api_output(request)
    log.verbose("HTTP-API CALL[%s]: %s", method.upper(), out)

    return out


def login(uri, username, password, endpoint=None, authscheme='credentials'):
    if endpoint is None:
        endpoint = LOGIN_ENDPOINT
    out = call(
        uri, method='post', endpoint=endpoint,
        payload={
            'username': username,
            'password': password,
            'authscheme': authscheme
        }
    )
    log.debug("Current iRODS user: %s", out.get('b2safe_user'))
    return out.get('token'), out.get('b2safe_home')


def folder_content(folder_path):
    if not os.path.exists(folder_path):
        log.exit("%s does not exist", folder_path)

    import glob
    log.debug("Looking for directory '%s'", folder_path)
    files = glob.glob(os.path.join(folder_path, "*"))
    if len(files) < 1:
        log.exit("%s does not contain any file", folder_path)

    return files


def parse_irods_listing(response, directory):
    to_print = ''
    home_content = []
    for element in response:
        if len(element) < 1:
            continue
        # log.pp(element)
        name, obj = element.popitem()
        home_content.append(name)
        metadata = obj.get('metadata', {})
        objtype = metadata.get('object_type')
        to_print += "\n%s [%s]" % (name, objtype)

    if len(home_content) > 0:
        log.info("Directory %s current content: %s\n", directory, to_print)

    return home_content
