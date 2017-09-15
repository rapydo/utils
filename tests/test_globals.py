# -*- coding: utf-8 -*-

from utilities.globals import mem


def test():

    value = 'Hello World'
    mem.attribute = value.copy()
    assert mem.attribute == value
