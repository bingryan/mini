# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from config import *


class LoginForm(FlaskForm):
    """管理员登录表单"""
    name = StringField(
        label="账号",
        validators=[
            DataRequired("用户名")
        ],
        description="账号",
        render_kw={
            "class": "text",
            "placeholder": "用户名",
            "required": "required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "password",
            "placeholder": "密码",
            "required": "required"
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "aui-button aui-style aui-button-primary",
        }
    )

    @staticmethod
    def validate_account(field):
        account = field.data
        if USER_NAME != account:
            raise ValidationError("账号不存在！")


class CommandForm(FlaskForm):
    """项目增加列表"""
    name = StringField(
        label="项目名字",
        validators=[
            DataRequired("请输入项目名字")
        ],
        description="项目名字",
        render_kw={
            "class": "text form-control",
            "placeholder": "项目名字",
            "required": "required"
        }
    )
    url = StringField(
        label="请求URL",
        validators=[
            DataRequired("请输入webhook 触发的事情的url！")
        ],
        description="请求URL",
        render_kw={
            "class": "url form-control",
            "placeholder": "webhook 触发的事情的url",
            "required": "required"
        }
    )
    command = TextAreaField(
        label="部署命令",
        validators=[
            DataRequired("请输入部署命令")
        ],
        description="密码",
        render_kw={
            "class": "command form-control",
            "placeholder": "部署命令",
            "required": "required"
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("触发事件之后，发送给你邮件的邮箱！")
        ],
        description="触发事件之后，发送给你邮件的邮箱！",
        render_kw={
            "class": "email form-control",
            "placeholder": "请填入您的邮箱",
            "required": "required"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class EmailForm(FlaskForm):
    """邮箱增加列表"""
    username = StringField(
        label="username",
        validators=[
            DataRequired("username")
        ],
        description="username",
        render_kw={
            "class": "text form-control",
            "placeholder": "username",
            "required": "required"
        }
    )
    password = StringField(
        label="password",
        validators=[
            DataRequired("password")
        ],
        description="password",
        render_kw={
            "class": "url form-control",
            "placeholder": "paasword",
            "required": "required"
        }
    )
    smtpserver = StringField(
        label="smtpserver",
        validators=[
            DataRequired("smtpserver")
        ],
        description="smtpserver",
        render_kw={
            "class": "command form-control",
            "placeholder": "smtpserver",
            "required": "required"
        }
    )
    smtpport = StringField(
        label="smtpport",
        validators=[
            DataRequired("smtpport")
        ],
        description="smtpport",
        render_kw={
            "class": "email form-control",
            "placeholder": "smtpport",
            "required": "required"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )
