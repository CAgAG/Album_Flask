from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(80), primary_key=True)
    nickname = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=False)
    avatarPath = db.Column(db.Text(), nullable=True)
    selfIntro = db.Column(db.Text(), nullable=True)

    email = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f'user: {self.username}'


class UserStar(db.Model):
    __tablename__ = 'userstar'
    userStarId = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    picId = db.Column(db.Integer(), db.ForeignKey("picture.pictureId"))
    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    isStar = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'userstar: {self.username}'


class Picture(db.Model):
    __tablename__ = 'picture'
    pictureId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    pictureName = db.Column(db.Text(), nullable=False)
    picturePath = db.Column(db.Text(), nullable=False)
    starSum = db.Column(db.Integer(), nullable=False)
    visible = db.Column(db.Boolean, default=False, nullable=False)
    pictureIntro = db.Column(db.Text(), nullable=True)

    downloadSum = db.Column(db.Integer(), nullable=False, default=0)
    thumbnailPath = db.Column(db.Text(), nullable=True)

    crated = db.Column(db.DateTime, default=datetime.now)
    albumId = db.Column(db.Integer(), db.ForeignKey('album.albumId'))

    def __repr__(self):
        return f'picture: {self.pictureName}'


class Album(db.Model):
    __tablename__ = 'album'
    albumId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    albumName = db.Column(db.String(80), nullable=False)

    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    crated = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'album: {self.albumName}'


class Comment(db.Model):
    __tablename__ = 'comment'
    commentId = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    pictureId = db.Column(db.Integer(), db.ForeignKey("picture.pictureId"))
    comment = db.Column(db.Text(), nullable=True)

    crated = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'comment: {self.username}'
