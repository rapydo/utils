# -*- coding: utf-8 -*-

from utilities.cron import Schedule


def test():

    def job():
        print("PROVA")
        import sys
        sys.exit(1)

    my_interval = 15
    cron = Schedule(interval=my_interval)
    assert len(cron.list()) == 0

    cron.add(job, interval_type='seconds')
    jobs = cron.list()
    assert len(jobs) == 1

    next_job = jobs.pop()

    # verify that this job is every minute
    assert next_job.interval == my_interval
    assert str(next_job.period) == '0:00:%s' % my_interval

    # Context manager to manage the infinite loop?
    # cron.run()
