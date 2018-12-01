# -*- coding: utf-8 -*-
import random
import string


def get_random_name(lenght=12, prefix=""):
    rand = random.SystemRandom()
    charset = string.ascii_uppercase + string.digits

    tmp_name = prefix
    for _ in range(lenght):
        tmp_name += rand.choice(charset)
    return tmp_name
