#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Blueprint, render_template, request, send_from_directory, Flask, jsonify,make_response
from app.config import BaseConfig
from app.views.module.authenticate import authenticate, login_check
from app.views.module.modules.anitAV.mini import mimi
from app.views.module.modules.anitAV.psh import psObf
from functools import wraps
import logging, os

AnitAV = Blueprint('anitav', __name__)
app = Flask(__name__)


@AnitAV.route('/avcheck')
@login_check
def avcheck():
    return render_template('/AnitAV/avcheck.html')


@AnitAV.route('/mimikatz', methods=['GET', 'POST'])
@login_check
def mimikatz():
    if request.method == 'GET':
        return render_template('/AnitAV/mimikatz.html')
    else:
        UPLOAD_FOLDER = 'modules/anitAV/mimikatz'
        basepath = os.path.dirname(__file__)
        newfilename = 'mimikatz.exe'
        if 'file' not in request.files:
            logging.debug('No file part')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            logging.debug('No selected file')
            return jsonify({'code': '-1', 'filename': '', 'msg': 'No selected file'})
        else:
            try:
                origin_file_name = file.filename
                logging.debug('filename is %s' % origin_file_name)
                file_dir = os.path.join(basepath,UPLOAD_FOLDER)
                if os.path.exists(file_dir):
                    logging.debug('%s path exist' % file_dir)
                    pass
                else:
                    logging.debug('%s path not exist' % file_dir)
                    os.makedirs(file_dir)
                file.save(os.path.join(file_dir, newfilename))
                return jsonify({'code': 0, 'filename': origin_file_name, 'msg': 'save successfully'})
            except Exception as e:
                logging.debug(e)
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})


@AnitAV.route('/mimidown/<new_mimikatz>')
@login_check
def mimidown(new_mimikatz):
    mimi()
    basepath = os.path.dirname(__file__)
    UPLOAD_FOLDER = 'modules/anitAV/mimikatz'
    file_dir = os.path.join(basepath, UPLOAD_FOLDER)
    file_name = new_mimikatz
    return send_from_directory(file_dir,file_name,as_attachment=True)


@AnitAV.route('/shellcode')
@login_check
def shellcode():
    return render_template('/AnitAV/shellcode.html')


@AnitAV.route('/powershell', methods=['GET', 'POST'])
@login_check
def powershell():
    if request.method == 'GET':
        return render_template('/AnitAV/powershell.html')
    else:
        UPLOAD_FOLDER = 'modules/anitAV/powershell'
        basepath = os.path.dirname(__file__)
        newfilename = 'payload.ps1'
        if 'file' not in request.files:
            logging.debug('No file part')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            logging.debug('No selected file')
            return jsonify({'code': '-1', 'filename': '', 'msg': 'No selected file'})
        else:
            try:
                origin_file_name = file.filename
                logging.debug('filename is %s' % origin_file_name)
                file_dir = os.path.join(basepath,UPLOAD_FOLDER)
                if os.path.exists(file_dir):
                    logging.debug('%s path exist' % file_dir)
                    pass
                else:
                    logging.debug('%s path not exist' % file_dir)
                    os.makedirs(file_dir)
                file.save(os.path.join(file_dir, newfilename))
                return jsonify({'code': 0, 'filename': origin_file_name, 'msg': 'save successfully'})
            except Exception as e:
                logging.debug(e)
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
@AnitAV.route('/pshdown/<new_powershell>')
def pshdown(new_powershell):
    psObf()
    basepath = os.path.dirname(__file__)
    UPLOAD_FOLDER = 'modules/anitAV/powershell'
    file_dir = os.path.join(basepath, UPLOAD_FOLDER)
    file_name = new_powershell
    return send_from_directory(file_dir,file_name,as_attachment=True)