from app import db, models


def db_commit():
    try:
        db.session.commit()
    except Exception as e:
        return False
    return True


# -------------------------------user

def create_base_user(username: str, password: str):
    user = models.User()
    user.username = username
    user.password = password
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

    users = user.query.filter_by(username=username).all()
    if len(users) == 0:
        return False
    fuser = users[0]
    assert isinstance(fuser, models.User)
    fuser.nickname = nickname
    fuser.selfIntro = selfIntro
    fuser.email = email
    fuser.phone = phone
    db.session.update(fuser)
    db_commit()
    return fuser

# --------------------------------picture

def create_album(username: str, albumName: str):
    album = models.Album()
    album.albumName = albumName
    album.username = username
    db.session.add(album)
    db_commit()
    return album.albumId


def get_albumId(username: str, albumName: str):
    album = models.Album()
    albums = album.query.filter_by(username=username, albumName=albumName).all()
    if len(albums) == 0:
        return False
    return albums[0].albumId


def create_picture(path: str, filename: str, intro: str, visible=False, albumId=0):
    picture = models.Picture()

    picture.pictureName = filename
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
    return pictures[0].picturePath.lstrip('./app')


def get_picture_info(pic_id: str):
    picture = models.Picture()
    pictures = picture.query.filter_by(pictureId=pic_id).all()

    if len(pictures) == 0:
        return None
    return pictures[0]


def del_picture(pic_id: str):
    picture = models.Picture()
    pictures = picture.query.filter_by(pictureId=pic_id).all()

    if len(pictures) == 0:
        return False
    db.session.delete(pictures[0])
    db_commit()
    return True
