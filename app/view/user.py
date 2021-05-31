import datetime

from flask import Blueprint, render_template, \
    request, redirect, url_for, session, jsonify

from app import database
from app.view import resultCode

user = Blueprint('user', __name__)


@user.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    email = request.form.get("email")
    phone = request.form.get("phone")

    result = database.create_user(username=username, password=password, email=email, phone=phone)

    if result:
        return jsonify({
            "code": resultCode.success,
            'massage': "注册成功"
        })
    else:
        return jsonify({
            "code": resultCode.fail,
            'massage': "注册名被使用"
        })


@user.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if database.check_login(username=username, password=password):
        return jsonify({
            "code": resultCode.success,
            'massage': "登录成功"
        })
    return jsonify({
        "code": resultCode.fail,
        'massage': "登录失败"
    })
