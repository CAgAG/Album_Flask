import pymysql
from flask import Flask, render_template, send_file
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
    return "hello world!"

@app.route("/index")
def t_index():
    return render_template('index.html')

@app.route("/about")
def t_about():
    return render_template('about.html')

@app.route("/download_app")
def download_app():
    return send_file('./media/base.apk', as_attachment=True, attachment_filename='悦享.apk')

@app.route('/favicon.ico')
def favicon():
    return send_file('./static/favicon.ico', mimetype='image/vnd.microsoft.icon')

