# -*- coding: utf-8 -*-

"""
Sending e-mails in python

more info:
https://pymotw.com/3/smtplib/
"""

import smtplib
from email.mime.text import MIMEText
import os

from utilities.logs import get_logger

log = get_logger(__name__)

# TODO: remove env var
# TODO: configure HOST with gmail, search example online


def send_mail(body, subject, to_address=None, from_address=None):

    smtp_host = os.environ.get("SMTP_HOST")
    admin_email_address = os.environ.get("SMTP_ADMIN")

    if smtp_host is None:
        log.info("Skipping send email: smtp host not configured")
        return False

    if from_address is None:
        if admin_email_address is None:
            log.warning(
                "Unable to send: " +
                "both from address and default admin are missing")
            return False
        else:
            from_address = admin_email_address

    if to_address is None:
        log.warning("Unable to send: destination is missing")
        return False

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address

        s = smtplib.SMTP(smtp_host)
        s.send_message(msg)
        s.quit()

        log.debug("Mail sent to %s" % to_address)
        return True

    except BaseException as e:
        log.error(str(e))
        return False
