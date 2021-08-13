#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Blueprint, render_template, request, send_from_directory, Flask, jsonify,make_response
from app.config import BaseConfig
from app.views.module.authenticate import authenticate, login_check
from app.views.module.modules.assist.ftp.ftpBrute import ftpbrute
from app.views.module.modules.assist.POP.popBrute import popbrute
from app.views.module.modules.assist.smtp.smtpBrute import smtpbrute
from app.views.module.modules.assist.sql.sql_Brute import sqlbrute
from app.views.module.modules.assist.ssh.ssh_Brute import sshbrute
from app.views.module.modules.assist.telnet.telnet_Brute import telnetbrute
from functools import wraps
import logging, os

Assist = Blueprint('assist', __name__)
app = Flask(__name__)

@Assist.route('/brute',methods=['GET','POST'])
@login_check
def ProtocolBrute():
    if request.method == 'GET':
        return render_template('/assist/brute.html')
    else:
        host = request.form.get('host')
        protocol = request.form.get('xieyi')
        if protocol == 'FTP':
            username, passwprd = ftpbrute(host)
        elif protocol == 'POP':
            username, passwprd = popbrute(host)
        elif protocol == 'SMTP':
            username, passwprd = smtpbrute(host)
        elif protocol == 'SQL':
            username, passwprd = sqlbrute(host)
        elif protocol == 'SSH':
            username, passwprd = sshbrute(host)
        else:
            username, passwprd = telnetbrute(host)

        return render_template('/assist/brute.html',username=username,passwprd=passwprd)

