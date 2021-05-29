from app import app
from app.view.user import user
from app.view.picture import picture
from app.view.comment import comment

# 注册蓝图
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(picture, url_prefix='/picture')
app.register_blueprint(comment, url_prefix='/comment')