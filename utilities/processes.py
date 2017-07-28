# -*- coding: utf-8 -*-

import os
import psutil
from utilities.logs import get_logger

log = get_logger(__name__)


def find(prefix, suffixes=None, local_bin=False):

    current_pid = os.getpid()

    for pid in psutil.pids():

        if pid == current_pid or not psutil.pid_exists(pid):
            continue
        process = psutil.Process(pid)

        if process.name() == prefix:
            cmd = process.cmdline()

            if local_bin:
                check = False
                for word in cmd:
                    if '/usr/local/bin' in word:
                        check = True
                if not check:
                    continue

            if suffixes is not None:
                check = False
                for word in cmd:
                    if word in suffixes:
                        check = True
                if not check:
                    continue

            log.warning('Already existing')  # : %s' % cmd)
            return True

    return False
