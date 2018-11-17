#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser

BASE_DIR = os.path.dirname(__file__)


def closest_cfg(filename='mini.cfg', path='.', prevpath=None):
    """
    return the path  of the closest mini.cfg file
    :param filename: default  get file name
    :param path:
    :param prevpath:
    :return:
    """
    if path == prevpath:
        return ''

    path = os.path.abspath(path)
    cfgfile = os.path.join(path, filename)
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_cfg(os.path.dirname(path), path)


def get_config(filename='mini.cfg', path='.'):
    """
    more about read: https://docs.python.org/3/library/configparser.html
    :param filename:
    :param path:
    :return:
    """
    cfg = ConfigParser()
    path = os.path.join(BASE_DIR, path)
    cfg.read(closest_cfg(filename=filename, path=path))
    return cfg


def get_data_config(filename):
    configfile_name = os.path.join(BASE_DIR, 'data', filename)
    if not os.path.exists(configfile_name):
        raise Exception("file is not exist")
    cfg = ConfigParser()
    cfg.read(configfile_name, encoding='utf-8')
    return cfg


def write_cfg(filename, data_path='data', cfg=None):
    """
    write cfg to data/filename
    :param data_path:
    :param filename:
    :param cfg:
    :return:
    """
    configfile_name = os.path.join(BASE_DIR, data_path, filename)

    with open(configfile_name, mode="w+", encoding="utf-8") as file:
        cfg.write(file)


def remove_cfg(filename, data_path='data'):
    """
    rm cfg to data/filename
    :param data_path:
    :param filename:
    :param cfg:
    :return:
    """
    configfile_name = os.path.join(BASE_DIR, data_path, filename)
    try:
        os.unlink(configfile_name)
    except NotImplementedError as e:
        print(e)


def list_data_file():
    """
    list all file in data directory
    :return:
    """
    data_dir = os.path.join(BASE_DIR, 'data')
    return os.listdir(data_dir)


def email_util(receiver, msg):
    from email.mime.text import MIMEText
    from email.header import Header
    import smtplib

    msg = MIMEText(msg)
    msg['Subject'] = Header('[mini系统邮件]', 'utf-8')
    cfg = get_config()
    username = cfg.get('email', 'username')
    password = cfg.get('email', 'password')
    # 输入SMTP服务器地址:
    smtp_server = cfg.get('email', 'smtpserver')
    # 输入收件人地址:
    to_addr = receiver
    server = smtplib.SMTP_SSL(smtp_server, cfg.get('email', 'smtpport'))
    server.login(username, password)
    server.sendmail(username, [to_addr], msg.as_string())
    server.quit()


if __name__ == '__main__':
    cfg = get_data_config('ryan')
    print(cfg)