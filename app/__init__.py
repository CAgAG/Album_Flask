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
