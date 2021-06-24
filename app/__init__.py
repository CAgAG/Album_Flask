import pymysql
from flask import Flask, render_template, send_file, redirect
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

app = Flask(__name__)  # type: Flask
app.config.from_object('config')
# 实例化一个数据库对象
db = SQLAlchemy(app)

from . import models, blueprint_register

db.create_all()

@app.route("/")
def hello():
    return '<p>hello world!</p><p><a href="/index">首页</a></p>'

@app.route("/index")
def t_index():
    return render_template('index.html')

@app.route("/about")
def t_about():
    return render_template('about.html')

@app.route("/download_app")
def download_app():
    return redirect('https://cloud.189.cn/web/share?code=nAry6bJfeqiq', code=301)

@app.route('/favicon.ico')
def favicon():
    return send_file('./static/favicon.ico', mimetype='image/vnd.microsoft.icon')

