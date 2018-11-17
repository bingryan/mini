#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from . import home
from data import ProductDB
from flask import abort
from utils import email_util


@home.route('/<app_url>', methods=["GET", "POST"])
def push_app(app_url=None):
    assert app_url is not None, 'WEBHOOK URl IS NONE'
    pdb = ProductDB()

    file = [i for i in pdb.products if i.url == app_url]
    if len(file) < 1:
        abort(404)

    res = os.system(file[0].command)
    if res == 0:
        msg = '你的项目【%s】重新部署成功' % file[0].name
        email_util(receiver=file[0].email, msg=msg)
        return "yes"
    msg = '你的项目【%s】重新部署时出现问题，请检测' % file[0].name
    email_util(receiver=file[0].email, msg=msg)
    return 'no'


@home.route('/', methods=["GET", "POST"])
def index():
    return "hello"
