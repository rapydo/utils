# -*- coding: utf-8 -*-

"""
Sending e-mails in python

more info:
https://pymotw.com/3/smtplib/
"""

from smtplib import SMTP, SMTP_SSL, SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import pytz

from utilities.logs import get_logger

log = get_logger(__name__)

# TODO: configure HOST with gmail, search example online


def send_mail(body, subject,
              to_address, from_address,
              smtp_host='localhost', smtp_port=587,
              cc=None, bcc=None,
              username=None, password=None, html=False, plain_body=None):

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

        dest_addresses = [to_address]

        date_fmt = "%a, %b %d, %Y at %I:%M %p %z"
        if html:
            msg = MIMEMultipart('alternative')
        else:
            msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address
        if cc is None:
            pass
        elif isinstance(cc, str):
            msg['Cc'] = cc
            dest_addresses.append(cc.split(","))
        elif isinstance(cc, list):
            msg['Cc'] = ",".join(cc)
            dest_addresses.append(cc)
        else:
            log.warning("Invalid CC value: %s", cc)
            cc = None

        if bcc is None:
            pass
        elif isinstance(bcc, str):
            msg['Bcc'] = bcc
            dest_addresses.append(bcc.split(","))
        elif isinstance(bcc, list):
            msg['Bcc'] = ",".join(bcc)
            dest_addresses.append(bcc)
        else:
            log.warning("Invalid BCC value: %s", bcc)
            bcc = None

        msg['Date'] = datetime.datetime.now(pytz.utc).strftime(date_fmt)

        if html:
            if plain_body is None:
                log.warning("Plain body is none")
                plain_body = body
            part1 = MIMEText(plain_body, 'plain')
            part2 = MIMEText(body, 'html')
            msg.attach(part1)
            msg.attach(part2)

        ###################
        # https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
        if smtp_port == '465':
            smtp = SMTP_SSL()
        else:
            smtp = SMTP()
            # if this is 587 we might need also
            # smtp.starttls()

        ###################
        smtp.set_debuglevel(0)
        log.verbose("Connecting to %s:%s" % (smtp_host, smtp_port))
        smtp.connect(smtp_host, smtp_port)
        if username is not None and password is not None:
            log.verbose("Authenticating SMTP")
            smtp.login(username, password)

        try:
            log.verbose("Sending email to %s", to_address)

            smtp.sendmail(from_address, dest_addresses, msg.as_string())

            log.info("Successfully sent email to %s [cc=%s], [bcc=%s]",
                     to_address, cc, bcc)
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
