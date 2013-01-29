#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 3n1b.com

import smtplib
import sys
import email
from email.mime.text import MIMEText

charset = 'utf-8'

send_mail_user = '3n1b.com@gmail.com'
send_mail_pswd = 'Glj@2012'
get_mail_user = '3n1b.com@gmail.com'

def send(sub, content, reciver = get_mail_user):
    msg = email.mime.text.MIMEText(content,'html',charset)
    msg['Subject'] = email.Header.Header(sub,charset)
    msg['From'] = send_mail_user
    msg['to'] = to_adress = reciver
    try:
        stp = smtplib.SMTP("smtp.gmail.com",587)
        stp.ehlo()
        stp.starttls()
        stp.ehlo
        stp.login(send_mail_user,send_mail_pswd)
        stp.sendmail(send_mail_user,to_adress,msg.as_string())
        stp.close()
        return True
    except Exception,e:
        print(e)
        return False

