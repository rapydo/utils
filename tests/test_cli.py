# -*- coding: utf-8 -*-

from utilities.cli import App


def test():
    app = App()
    log = app.setup_logger()
    log.debug('App %s has a logger %s', app, log)

    # context manager? how does invoke run tests?
    # app.run()
    assert True
