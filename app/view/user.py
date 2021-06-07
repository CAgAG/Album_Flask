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

    result = database.create_base_user(username=username, password=password, email=email, phone=phone)

    if result:
        return jsonify(resultCode.success_message(message='注册成功'))
    else:
        return jsonify(resultCode.fail_message(message='注册名被使用'))


@user.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if database.check_login(username=username, password=password):
        return jsonify(resultCode.success_message(message='登录成功'))
    return jsonify(resultCode.fail_message(message='登录失败'))


@user.route('/show_user_info', methods=['POST'])
def show_user_info():
    username = request.form.get("username")

    user = database.get_user_info(username=username)
    if not user:
        return jsonify(resultCode.fail_message(message='没有该用户'))

    data = {
        'nickname': user.nickname,
        'avatarPath': user.avatarPath,
        'selfIntro': user.selfIntro,
        'email': user.email,
        'phone': user.phone
    }
    return jsonify(resultCode.success_message(message='查询成功', data=data))


@user.route('/change_user_info', methods=['POST'])
def change_user_info():
    username = request.form.get("username")
    nickname = request.form.get('nickname')
    selfIntro = request.form.get('selfIntro')
    email = request.form.get('email')
    phone = request.form.get('phone')

    user = database.change_user_info(username=username, nickname=nickname, selfIntro=selfIntro,
                                     email=email, phone=phone)
    if not user:
        return jsonify(resultCode.fail_message(message='没有该用户'))

    return jsonify(resultCode.success_message(message='修改成功'))
