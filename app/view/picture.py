import datetime

from flask import Blueprint, render_template, \
    request, redirect, url_for, session

from app import database

picture = Blueprint('picture', __name__)