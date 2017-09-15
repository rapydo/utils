# -*- coding: utf-8 -*-

"""
A python cron for jobs/functions

Examples:
http://schedule.readthedocs.io/en/stable/#usage
"""

from utilities.logs import get_logger
log = get_logger(__name__)

try:
    import schedule
except ImportError as e:
    log.exit("\nThis module requires an extra package:\n%s", e)


class Schedule(object):
    """ A python cron to satisfy your schedules """

    def __init__(self, interval=1):
        # super(Schedule, self).__init__()

        self._cron = schedule
        self.interval = interval

    def add(self, function, parameters=None, interval_type="minutes"):
        if interval_type == 'minutes':
            return self._cron.every(self.interval).minutes.do(function)
        else:
            return self._cron.every(self.interval).seconds.do(function)

    def list(self):
        log.info("Jobs:\n%s", self._cron.jobs)

    def run(self):
        import time
        while True:
            self._cron.run_pending()
            time.sleep(1)
