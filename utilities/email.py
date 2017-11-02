# -*- coding: utf-8 -*-

"""
Sending e-mails in python

more info:
https://pymotw.com/3/smtplib/
"""

from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
import datetime

from utilities.logs import get_logger

log = get_logger(__name__)

# TODO: configure HOST with gmail, search example online


def send_mail(body, subject,
              to_address, from_address,
              smtp_host='localhost', smtp_port=587,
              username=None, password=None):

    if smtp_host is None:
        log.error("Skipping send email: smtp host not configured")
        return False

    if from_address is None:
        log.error("Skipping send email: from address not configured")
        return False

    if to_address is None:
        log.error("Skipping send email: destination address not configured")
        return False

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Date'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        smtp = SMTP()
        smtp.set_debuglevel(0)
        log.verbose("Connecting to %s:%s" % (smtp_host, smtp_port))
        smtp.connect(smtp_host, smtp_port)
        if username is not None and password is not None:
            log.verbose("Authenticating SMTP")
            smtp.login(username, password)

        try:
            log.verbose("Sending email to %s", to_address)
            smtp.sendmail(from_address, to_address, msg)
            log.info("Successfully sent email to %s", to_address)
            smtp.quit()
            return True
        except SMTPException:
            log.error("Unable to send email to %s", to_address)
            smtp.quit()
            return False

    except BaseException as e:
        log.error(str(e))
        return False

    return False
