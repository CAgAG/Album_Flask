from app import db, models


def db_commit():
    try:
        db.session.commit()
    except Exception as e:
        return False
    return True


def create_base_user(username: str, password: str):
    user = models.User()
    user.username = username
    user.password = password
    db.session.add(user)
    return db_commit()


def create_user(username: str, password: str, email: str, phone: str):
    user = models.User()
    user.username = username
    user.password = password
    user.email = email
    user.password = password
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


