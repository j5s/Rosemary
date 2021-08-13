from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from app import app
from app.views.module.authenticate import authenticate,login_check
from app.views.module.priv_lege import privlege
from app.views.module.anit_av import AnitAV
from app.views.module.bpass_waf import BypassWAF
from app.views.module.assist import Assist
from random import sample
from string import digits, ascii_lowercase


@app.route('/')
@login_check
def test():
    return render_template('base.html')

app.register_blueprint(authenticate)
app.register_blueprint(privlege)
app.register_blueprint(AnitAV)
app.register_blueprint(BypassWAF)
app.register_blueprint(Assist)

@app.errorhandler(404)
@login_check
def page_not_found(e):
    return render_template('/404/index.html')

@app.errorhandler(500)
@login_check
def page_server_error(e):
    return render_template('/500/index.html')