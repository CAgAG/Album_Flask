import datetime

from flask import Blueprint, render_template, \
    request, redirect, url_for, session

from app import database

comment = Blueprint('comment', __name__)