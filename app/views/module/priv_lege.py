#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Blueprint, render_template, request, redirect, url_for, Flask, session
from app.config import BaseConfig
from app.views.module.authenticate import authenticate,login_check
from functools import wraps
from app.views.module.modules.privlege import lin_priv

privlege = Blueprint('privlege', __name__)
app = Flask(__name__)

@privlege.route('/linux-priv',methods=['GET','POST'])
@login_check
def linuxpriv():
    if request.method == "GET":
        return render_template('/privs/linuxprv.html')
    else:
        version = request.form.get('version')
        name = lin_priv.lin_exploit(version)
        return render_template('/privs/linuxprv.html',name=name[0],cve=name[1],src=name[2])

@privlege.route('/win-priv')
@login_check
def avcheck():
    return render_template('/privs/winprv.html')