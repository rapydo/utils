# -*- coding: utf-8 -*-
import random
import string


def get_random_name(len=12, prefix=""):
    rand = random.SystemRandom()
    charset = string.ascii_uppercase + string.digits

    tmp_name = prefix
    for _ in range(len):
        tmp_name += rand.choice(charset)
    return tmp_name
