import datetime

from flask import Blueprint, render_template, \
    request, redirect, url_for, session, jsonify

from app import database
from app.view import resultCode

comment = Blueprint('comment', __name__)


@comment.route('/add', methods=['POST'])
def comment_add():
    username = request.form.get('username')
    pic_id = request.form.get('pic_id')
    content = request.form.get('content')

    result = database.add_comment(username=username, pic_id=int(pic_id), content=content)
    if result is None:
        return jsonify(resultCode.fail_message(message='评论失败'))
    return jsonify(resultCode.success_message(message='评论成功'))


@comment.route('/show_comment/<pic_id>', methods=['GET'])
def show_comment(pic_id: str):
    result = database.show_comment(pic_id=int(pic_id))
    if len(result) == 0:
        return jsonify(resultCode.fail_message(message='无评论', data=result))
    return jsonify(resultCode.success_message(message='查询成功', data=result))
