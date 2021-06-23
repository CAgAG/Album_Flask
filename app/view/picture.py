import datetime, os, uuid

from flask import Blueprint, render_template, \
    request, redirect, url_for, session, jsonify, send_file
from werkzeug.utils import secure_filename

from app import database
from app.view import resultCode, UPLOAD_PATH, BASEURL, spider

picture = Blueprint('picture', __name__)


def to_boolean(s: str):
    if s.lower() == 'true':
        return True
    else:
        return False


@picture.route('/create_album', methods=['POST'])
def create_album():
    username = request.form.get('username')
    album_name = request.form.get('albumName')

    try:
        id = database.create_album(username=username, albumName=album_name)

        data = {
            'album_id': id
        }
        return jsonify(resultCode.success_message(message='创建成功', data=data))
    except Exception:
        return jsonify(resultCode.fail_message(message='创建失败'))


@picture.route('/upload', methods=['POST'])
def upload_picture():
    file = request.files['file']
    filename = request.form.get('filename')
    filetype = file.content_type.lstrip('image/')
    username = request.form.get('username')

    intro = request.form.get('intro')
    visible = to_boolean(request.form.get('visible'))

    albumId = database.get_albumId(username=username, albumName=request.form.get('albumName'))

    unique_path = os.path.join(username, datetime.datetime.now().strftime('%F-%H'))
    path = os.path.join(UPLOAD_PATH, unique_path)
    if not os.path.exists(path):
        os.makedirs(path)

    filepath = os.path.join(path, str(uuid.uuid4()) + '.' + filetype)

    try:
        file.save(filepath)
        pic_id = database.create_picture(path=filepath, filename=filename + '.' + filetype, intro=intro,
                                         visible=visible,
                                         albumId=albumId)

        data = {
            'picture_id': pic_id
        }

        return jsonify(resultCode.success_message(message='上传成功', data=data))
    except Exception:
        print('=====================')
        print('filetype: ', filetype)
        print('filepath: ', filepath)
        print('intro: ', intro)
        if file is None:
            print("未接收到图片")
        print('=====================')
        return jsonify(resultCode.fail_message(message='上传失败'))


@picture.route('/show_albums', methods=['POST'])
def show_albums():
    username = request.form.get('username')

    try:
        albums = database.show_all_user_albumName(username=username)
        return jsonify(resultCode.success_message(message='查询成功', data=albums))
    except Exception:
        return jsonify(resultCode.fail_message(message='查询失败'))


@picture.route('/show_album_pictures', methods=['POST'])
def show_album_pictures():
    username = request.form.get('username')
    albumName = request.form.get('albumName')

    try:
        pictureIds = database.show_album_picturesId(username=username, albumName=albumName)
        return jsonify(resultCode.success_message(message='查询成功', data=pictureIds))
    except Exception:
        return jsonify(resultCode.fail_message(message='查询失败'))


@picture.route('/show_picture/<path:pic_id>', methods=['GET'])
def show_picture(pic_id: str):
    pic_path = database.get_picture_path(pic_id=pic_id)
    if pic_path is None:
        return jsonify(resultCode.fail_message(message='没有图片资源'))
    return send_file(pic_path)


@picture.route('/show_picture_info', methods=['POST'])
def show_picture_info():
    pic_id = request.form.get('pic_id')

    picture = database.get_picture_info(pic_id=pic_id)
    if picture is None:
        return jsonify(resultCode.fail_message(message='没有图片信息'))

    username = database.get_username_by_picId(pic_id=pic_id)
    data = {
        'pictureName': picture.pictureName,
        'starSum': picture.starSum,
        'visible': picture.visible,
        'pictureIntro': picture.pictureIntro,
        'downloadSum': picture.downloadSum,
        'thumbnailPath': picture.thumbnailPath,
        'created': picture.crated,
        'comment_url': '{}/comment/show_comment/'.format(BASEURL) + pic_id,
        'picture_url': '{}/picture/show_picture/'.format(BASEURL) + pic_id,
        'avatar_url': f'{BASEURL}/user/show_avatar/{username}',
        'nickName': database.get_nickName(username=username)
    }
    return jsonify(resultCode.success_message(message='查询成功', data=data))


@picture.route('/del', methods=['POST'])
def del_picture():
    pic_id = request.form.get('pic_id')

    pic_path = database.get_picture_path(pic_id=pic_id)
    is_del = database.del_picture(pic_id=pic_id)
    if not is_del:
        return jsonify(resultCode.fail_message(message='删除失败'))

    os.remove(os.path.join('./app/', pic_path))
    return jsonify(resultCode.success_message(message='删除成功'))


@picture.route('/index', methods=['POST'])
def index():
    username = request.form.get('username')
    page = request.form.get('page')
    num = request.form.get('num')

    p_info = database.show_visible_picture(cur_username=username, page=int(page), num=int(num))
    return jsonify(resultCode.success_message(message='查询成功', data=p_info))


@picture.route('/del_album', methods=['POST'])
def del_album():
    username = request.form.get('username')
    albumName = request.form.get('albumName')

    is_del = database.delete_album(username=username, albumName=albumName)
    if is_del is None:
        return jsonify(resultCode.fail_message(message='删除失败'))

    for path in is_del:
        os.remove(os.path.join('./app/', path))
    return jsonify(resultCode.success_message(message='删除成功'))


@picture.route('/baidu_index', methods=['POST'])
def baidu_index():
    page = request.form.get('page')
    num = request.form.get('num')
    keyword = request.form.get('keyword')

    p_info = spider.spider_baidu(page=int(page), num=int(num), keyword=keyword)
    return jsonify(resultCode.success_message(message='查询成功', data=p_info))


@picture.route('/douban_rank', methods=['POST'])
def douban_rank():
    p_info = spider.spider_doban()
    return jsonify(resultCode.success_message(message='查询成功', data=p_info))


@picture.route('/wallpaper_rank', methods=['POST'])
def wallpaper_rank():
    p_info = spider.spider_netbian()
    return jsonify(resultCode.success_message(message='查询成功', data=p_info))
