# -*- coding: utf-8 -*-

from utilities.random import get_random_name


def test():

    s1 = get_random_name()
    s2 = get_random_name()

    assert s1 != s2

    s1 = get_random_name(lenght=10)
    s2 = get_random_name(lenght=20)

    assert len(s1) == 10
    assert len(s2) == 20

    s1 = get_random_name(prefix='TEST_')

    assert s1.startswith('TEST_')

    s1 = get_random_name(lenght=0)
    assert s1 == ""

    s1 = get_random_name(lenght=0, prefix='TEST')
    assert s1 == "TEST"
