#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, session, request
from configparser import ConfigParser
from . import admin
from app.admin.forms import LoginForm, CommandForm, EmailForm
from config import *
import uuid
import time
from utils import write_cfg, list_data_file, remove_cfg, get_data_config, get_config
from data import ProductDB, EmailInfo


@admin.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        if data["name"] != USER_NAME or data["pwd"] != PASS_WD:
            flash("账号或密码错误", "err")
            return redirect(url_for('admin.login'))
        session["user_name"] = data['name']
        session["user_id"] = uuid.uuid1().hex
        return render_template('admin/admin.html')
    return render_template('admin/login.html', form=form)


@admin.route('/email/add/', methods=["GET", "POST"])
def email_add():
    form = EmailForm()
    if form.validate_on_submit():
        data = form.data
        username = data['username']
        password = data['password']
        smtpserver = data['smtpserver']
        smtpport = data['smtpport']
        Config = ConfigParser()
        Config.add_section('email')
        Config.set("email", "username", username)
        Config.set("email", "password", password)
        Config.set("email", "smtpserver", smtpserver)
        Config.set("email", "smtpport", smtpport)
        write_cfg(filename='mini.cfg', data_path='.', cfg=Config)
        flash("增加项目成功", "success")
        return redirect(url_for('admin.email_add'))
    return render_template("admin/email_add.html", form=form)


@admin.route('/email/list/', methods=["GET", "POST"])
def email_list():
    # Render file
    cfg = get_config()
    page_data = EmailInfo(
        username=cfg.get("email", 'username'),
        password=cfg.get("email", 'password'),
        smtpserver=cfg.get("email", 'smtpserver'),
        smtpport=cfg.get("email", 'smtpport'),
    )
    return render_template("admin/email_list.html", v=page_data)


# 编辑邮箱
@admin.route("/email/edit/", methods=["GET", "POST"])
def email_edit(name='mini.cfg'):
    form = EmailForm()
    # 获得当前的编辑object
    cfg = get_config(name)
    if request.method == "GET":
        form.username.data = cfg.get('email', 'username')
        form.password.data = cfg.get('email', 'password')
        form.smtpserver.data = cfg.get('email', 'smtpserver')
        form.smtpport.data = cfg.get('email', 'smtpport')
    if form.validate_on_submit():
        data = form.data
        Config = ConfigParser()
        Config.add_section("email")
        Config.set("email", "username", data['username'])
        Config.set("email", "password", data['password'])
        Config.set("email", "smtpserver", data['smtpserver'])
        Config.set("email", "smtpport", data['smtpport'])
        write_cfg(filename='mini.cfg', data_path='.', cfg=Config)
        flash("修改项目成功！", "success")
        return redirect(url_for('admin.email_edit', name=name))
    return render_template("admin/email_edit.html", form=form, name=name)


@admin.route('/product/add/', methods=["GET", "POST"])
def product_add():
    """
    对提交的项目数据进行更新
    """
    form = CommandForm()
    if form.validate_on_submit():
        data = form.data
        # 判断编辑的信息是否存在
        # 项目名字是否存在
        if data['name'] in list_data_file():
            flash("项目名已经存在", "err")
            return redirect(url_for('admin.product_add'))
        # webhooks的url 是否存在
        pdb = ProductDB()
        if data['url'] in [i.url for i in pdb.products]:
            flash("webhooks触发URl已经存在", "err")
            return redirect(url_for('admin.product_add'))

        url = data['url']
        command = str(data['command'].split('\n'))
        email = data['email']
        section_name = data['name']
        Config = ConfigParser()
        Config.add_section(section_name)
        Config.set(section_name, "name", section_name)
        Config.set(section_name, "time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        Config.set(section_name, "url", url)
        Config.set(section_name, "command", command)
        Config.set(section_name, "email", email)
        write_cfg(filename=section_name, cfg=Config)
        flash("增加项目成功", "success")
        return redirect(url_for('admin.product_add'))
    return render_template("admin/product_add.html", form=form)


@admin.route('/product/list/<int:page>/', methods=["GET", "POST"])
def product_list(page=None):
    """
    列出全部的项目信息
    问题：
        1、如果对data 目录下面的cfg进行读取合并为一个变量进行前端的绚染
        2、如何分页
    :return:
    """
    if page is None:
        page = 1
    # Render file
    pdb = ProductDB()
    page_data = pdb.paginate(page=page, per_page=10)
    return render_template("admin/product_list.html", page_data=page_data)


# 删除项目
@admin.route("/product/del/<string:name>/", methods=["GET", "POST"])
def product_del(name=None):
    # 删除 data 下面的某个项目
    assert name is not None, '删除项目不存在'
    remove_cfg(name)
    flash("删除项目成功！", "success")
    return redirect(url_for('admin.product_list', page=1))


# 编辑项目
@admin.route("/product/edit/<string:name>/", methods=["GET", "POST"])
def product_edit(name=None):
    form = CommandForm()
    # 获得当前的编辑object
    cfg = get_data_config(name)
    if request.method == "GET":
        form.name.data = name
        form.command.data = cfg.get(name, 'command')
        form.email.data = cfg.get(name, 'email')
        form.url.data = cfg.get(name, 'url')
    if form.validate_on_submit():
        data = form.data
        # 判断编辑的信息是否存在
        # 项目名字是否存在
        if data['name'] in list_data_file():
            flash("项目名已经存在", "err")
            return redirect(url_for('admin.product_edit', name=name))
        # webhooks的url 是否存在
        pdb = ProductDB()
        if data['url'] in [i.url for i in pdb.products]:
            flash("webhooks触发URl已经存在", "err")
            return redirect(url_for('admin.product_edit', name=name))

        Config = ConfigParser()
        Config.add_section(name)
        Config.set(name, "name", name)
        Config.set(name, "time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        Config.set(name, "url", data['url'])
        Config.set(name, "command", data['command'])
        Config.set(name, "email", data['email'])
        write_cfg(filename=name, cfg=Config)
        flash("修改项目成功！", "success")
        return redirect(url_for('admin.product_edit', name=name))
    return render_template("admin/product_edit.html", form=form, name=name)
