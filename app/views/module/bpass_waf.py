#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, send_from_directory, Flask, jsonify,make_response
from app.config import BaseConfig
from app.views.module.authenticate import authenticate, login_check
from app.views.module.modules.BypassWaf.bypass import create_rs_data
from app.views.module.modules.BypassWaf.sqlibypass import CommentBypass,Utf16Bypass,JsonBypass,EvtBypass,Bypass360,BypassDog,BypassDun,BypassLua,BypassYsuo
from functools import wraps
import logging, os

BypassWAF = Blueprint('bypasswaf', __name__)
app = Flask(__name__)

@BypassWAF.route('/wafbypass',methods=['GET','POST'])
@login_check
def waf_bypass():
    if request.method == 'GET':
        return render_template('/BypassWaf/bypass.html')
    else:
        payload = request.form.get('payload')
        data = create_rs_data(payload)
        return render_template('/BypassWaf/bypass.html',exp=data)

@BypassWAF.route('/sqlbypass',methods=['GET','POST'])
def sql_bypass():
    if request.method == 'GET':
        return render_template('/BypassWaf/sqlbypass.html')
    else:
        exploit = ""
        payload = request.form.get('bypass')
        if payload == "CommentBypass":
            exploit = CommentBypass()
        elif payload == "Utf16Bypass":
            exploit = Utf16Bypass()
        elif payload == "JsonBypass":
            exploit = JsonBypass()
        elif payload == "EvtBypass":
            exploit = EvtBypass()
        elif payload == "Bypass360":
            exploit = Bypass360()
        elif payload == "BypassDog":
            exploit = BypassDog()
        elif payload == "BypassDun":
            exploit = BypassDun()
        elif payload == "BypassLua":
            exploit = BypassLua()
        else:
            exploit = BypassYsuo()
        return render_template('/BypassWaf/sqlbypass.html',exp=exploit)

@BypassWAF.route('/amsibypass')
def asmibypass():
    if request.method == 'GET':
        return render_template('/BypassWaf/amsibypass.html')