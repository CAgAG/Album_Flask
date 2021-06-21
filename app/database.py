from app import db, models
from app.view import BASEURL


def db_commit():
    try:
        db.session.commit()
    except Exception as e:
        print("提交发送错误： ", e)
        return False
    return True


# -------------------------------user

def create_base_user(username: str, password: str, email: str, phone: str):
    user = models.User()
    user.username = username
    user.nickname = username
    user.password = password
    user.email = email
    user.phone = phone
    db.session.add(user)
    return db_commit()


def check_login(username: str, password: str):
    user = models.User()

    users = user.query.filter_by(username=username).all()
    if len(users) == 0:
        return False
    fuser = users[0]
    if fuser.password == password:
        return True
    return False


def get_user_info(username: str):
    user = models.User()

    users = user.query.filter_by(username=username).all()
    if len(users) == 0:
        return False
    fuser = users[0]
    return fuser


def change_user_info(username: str, nickname: str, selfIntro: str, email: str, phone: str):
    user = models.User()

    user = user.query.filter_by(username=username)
    if len(user.all()) == 0:
        return False

    args = {
        'nickname': nickname,
        'selfIntro': selfIntro,
        'email': email,
        'phone': phone
    }
    user.update(args)
    db_commit()
    return user


def change_user_avatar(username: str, avatarPath: str):
    user = models.User()

    user = user.query.filter_by(username=username)
    if len(user.all()) == 0:
        return False

    args = {
        'avatarPath': avatarPath,
    }
    user.update(args)
    db_commit()
    return user


def change_star(username: str, picId: str):
    user_star = models.UserStar()
    picture = models.Picture()

    user_star_query = user_star.query.filter_by(username=username, picId=picId)
    try:
        if len(user_star_query.all()) == 0:
            assert isinstance(user_star, models.UserStar)
            user_star.username = username
            user_star.picId = picId
            user_star.isStar = False
            db.session.add(user_star)
            db_commit()
            user_star_query = user_star
        else:
            user_star_query = user_star_query.first()

        user_star_query.isStar = not user_star_query.isStar
        pr = picture.query.filter_by(pictureId=picId).first()
        if user_star_query.isStar:
            pr.starSum += 1
        else:
            pr.starSum -= 1
        db_commit()
        return True
    except Exception:
        print('update star 失败')
        return False


def is_star(username: str, picId: str):
    user_star = models.UserStar()

    user_star_query = user_star.query.filter_by(username=username, picId=picId).first()
    if user_star_query is None:
        return False
    return user_star_query.isStar


def get_nickName(username: str):
    user = models.User()

    user = user.query.filter_by(username=username)
    if len(user.all()) == 0:
        return ''

    return user.first().nickname


# --------------------------------picture

def create_album(username: str, albumName: str):
    album = models.Album()
    album.albumName = albumName
    album.username = username

    albums = album.query.filter_by(albumName=albumName, username=username).all()
    if len(albums) == 0:
        db.session.add(album)
        db_commit()
        return album.albumId
    else:
        return albums[0].albumId


def get_albumId(username: str, albumName: str):
    album = models.Album()
    albums = album.query.filter_by(username=username, albumName=albumName).all()
    if len(albums) == 0:
        return False
    return albums[0].albumId


def create_picture(path: str, filename: str, intro: str, visible=False, albumId=0):
    picture = models.Picture()

    picture.pictureName = filename.replace('..', '.')
    picture.picturePath = path
    picture.pictureIntro = intro
    picture.visible = visible
    picture.albumId = albumId
    picture.downloadSum = 0
    picture.starSum = 0

    db.session.add(picture)
    db_commit()
    return picture.pictureId


def show_all_user_albumName(username: str):
    album = models.Album()
    albums = album.query.filter_by(username=username).all()

    ret = []
    for a in albums:
        ret.append(a.albumName)
    return ret


def show_album_picturesId(username: str, albumName: str):
    albumId = get_albumId(username=username, albumName=albumName)

    picture = models.Picture()
    pictures = picture.query.filter_by(albumId=albumId).all()

    ret = []
    for p in pictures:
        ret.append(p.pictureId)
    return ret


def get_picture_path(pic_id: str):
    picture = models.Picture()
    pictures = picture.query.filter_by(pictureId=pic_id).all()

    if len(pictures) == 0:
        return None
    return pictures[0].picturePath.lstrip('./app/')


def get_picture_info(pic_id: str):
    picture = models.Picture()
    pictures = picture.query.filter_by(pictureId=pic_id).all()

    if len(pictures) == 0:
        return None
    return pictures[0]


def del_picture(pic_id: str):
    picture = models.Picture()
    comment = models.Comment()
    comments = comment.query.filter_by(pictureId=pic_id).all()
    pictures = picture.query.filter_by(pictureId=pic_id).all()

    if len(pictures) == 0:
        return False
    for c in comments:
        db.session.delete(c)
    db_commit()
    db.session.delete(pictures[0])
    db_commit()
    return True


def show_visible_picture(cur_username: str, page: int, num: int):
    picture = models.Picture()
    album = models.Album()
    pictures = picture.query.filter_by(visible=True).order_by(models.Picture.crated.desc()).paginate(page=page,
                                                                                                     per_page=num).items

    rets = []
    for p in pictures:
        pic_name = p.pictureName
        # pic_path = p.picturePath
        pic_starSum = p.starSum
        pic_id = p.pictureId

        pic_albumId = p.albumId
        unique_album = album.query.filter_by(albumId=pic_albumId).first()
        username = unique_album.username
        nickName = get_nickName(username=username)
        isStar = is_star(username=cur_username, picId=pic_id)
        if nickName is None:
            nickName = username

        data = {
            'pic_url': '{}/picture/show_picture/'.format(BASEURL) + str(pic_id),
            'avatar_url': '{}/user/show_avatar/'.format(BASEURL) + str(username),
            'pic_name': pic_name.split('.')[0],
            'pic_id': pic_id,
            'pic_starSum': pic_starSum,
            'username': nickName,
            'albumName': unique_album.albumName,
            'downloadSum': p.downloadSum,
            'is_star': isStar
        }
        rets.append(data)

    return rets


def get_avatar_path(username: str):
    user = models.User()
    users = user.query.filter_by(username=username).all()

    if len(users) == 0:
        return None
    return users[0].avatarPath.lstrip('./app')


def delete_album(username: str, albumName: str):
    albumId = get_albumId(username=username, albumName=albumName)

    album = models.Album()
    picture = models.Picture()

    a = album.query.filter_by(albumId=albumId).first()
    ps = picture.query.filter_by(albumId=albumId).all()
    if a is None:
        return None
    ret = []
    for p in ps:
        db.session.delete(p)
        ret.append(p.picturePath)
    db_commit()
    db.session.delete(a)
    db_commit()
    return ret


# --------------------------------------------- comment
def add_comment(username: str, pic_id: int, content: str):
    comment = models.Comment()

    comment.username = username
    comment.pictureId = pic_id
    comment.comment = content

    db.session.add(comment)
    db_commit()
    return comment.commentId


def show_comment(pic_id: int):
    comment = models.Comment()

    comments = comment.query.filter_by(pictureId=pic_id).all()

    rets = []
    for c in comments:
        ret = {}
        assert isinstance(c, models.Comment)
        ret['comment_id'] = c.commentId
        ret['nickName'] = get_nickName(username=c.username)
        ret['content'] = c.comment
        ret['date'] = c.crated

        rets.append(ret)
    return rets


def delete_comment(comment_id: int):
    comment = models.Comment()
    c = comment.query.filter_by(commentId=comment_id).first()
    if c is None:
        return None
    cId = c.commentId
    db.session.delete(c)
    db_commit()
    return cId
