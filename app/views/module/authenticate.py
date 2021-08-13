#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Blueprint, render_template, request, redirect, url_for, Flask, session
from app.config import BaseConfig
from functools import wraps

authenticate = Blueprint('authenticate', __name__)
app = Flask(__name__)


@authenticate.route('/login', methods=['GET', 'POST'])
def login_view():
    # login view
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if password == BaseConfig.WEB_PASS and username == BaseConfig.WEB_USER:
            try:
                session['login'] = 'A1akPTQJiz9wi9yo4rDz8ubM1b1'
                return render_template('base.html')
            except Exception as e:
                print(e)
                return render_template('/login/login.html', msg="Internal Server Error")
        else:
            return render_template('/login/login.html', msg="Invalid Password")
    return render_template('/login/login.html')


# login-out
@authenticate.route('/login-out')
def login_out():
    session['login'] = ''
    return redirect(url_for('authenticate.login_view'))


# login-check
def login_check(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if "login" in session:
                if session['login'] == 'A1akPTQJiz9wi9yo4rDz8ubM1b1':
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for('authenticate.login_view'))
            else:
                return redirect(url_for('authenticate.login_view'))
        except Exception as e:
            return redirect(url_for('authenticate.login_view'))
    return wrapper
