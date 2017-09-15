# -*- coding: utf-8 -*-

from utilities import apiclient


def test():
    log = apiclient.setup_logger(__name__, 'info')
    log.info('Client has a logger')

    assert not apiclient.check_cli_arg()

    # NOTE: to complete this tests we should have some HTTP API in place
    assert apiclient.call('http://localhost', exit_on_fail=False) is None
