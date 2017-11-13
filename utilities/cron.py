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

    def add(self, function, interval_type="minutes"):
        if interval_type == 'minutes':
            return self._cron.every(self.interval).minutes.do(function)
        elif interval_type == 'seconds':
            return self._cron.every(self.interval).seconds.do(function)
        else:
            log.exit("Unhandled interval type: %s", interval_type)

    def list(self):
        log.info("Jobs:\n%s", self._cron.jobs)
        return self._cron.jobs

    def run(self):

        import time

        while True:

            # FIXME: this is a draft catching exceptions,
            # to be further tested and improved
            try:
                self._cron.run_pending()
            except BaseException as e:
                etype = e.__class__.__name__
                if etype == 'KeyboardInterrupt':
                    log.exit("Killed by user")
                log.warning(
                    "Failed to execute cron job\n%s(%s)", etype, e)

            time.sleep(1)
