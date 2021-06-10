import datetime, os, uuid

from flask import Blueprint, render_template, \
    request, redirect, url_for, session, jsonify, send_file

from app import database
from app.view import resultCode, UPLOAD_PATH

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


@user.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    username = request.form.get("username")
    file = request.files['file']
    filetype = file.content_type.lstrip('image/')

    path = os.path.join(UPLOAD_PATH, username)
    if not os.path.exists(path):
        os.makedirs(path)

    filepath = os.path.join(path, str(uuid.uuid4()) + '.' + filetype)

    try:
        file.save(filepath)
        database.change_user_avatar(username=username, avatarPath=filepath)

        return jsonify(resultCode.success_message(message='上传成功'))
    except Exception:
        return jsonify(resultCode.fail_message(message='上传失败'))


@user.route('/show_avatar/<path:username>', methods=['GET'])
def show_picture(username: str):
    pic_path = database.get_avatar_path(username=username)
    if pic_path is None:
        return jsonify(resultCode.fail_message(message='没有图片资源'))
    return send_file(pic_path)


@user.route('/change_star_picture', methods=['POST'])
def change_star_picture():
    username = request.form.get("username")
    picId = request.form.get("picId")

    if database.change_star(username=username, picId=picId):
        return jsonify(resultCode.success_message(message='改变star成功'))
    return jsonify(resultCode.fail_message(message='改变star失败'))


@user.route('/picture_is_star', methods=['POST'])
def picture_is_star():
    username = request.form.get("username")
    picId = request.form.get("picId")

    try:
        result = database.is_star(username=username, picId=picId)
        ctx = {
            'is_star': result
        }
        return jsonify(resultCode.success_message(message='查询成功', data=ctx))
    except Exception:
        return jsonify(resultCode.success_message(message='查询失败'))

