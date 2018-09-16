# -*- coding: utf-8 -*-

import os
from datetime import timedelta

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'wiedb'
USERNAME = 'root'
PASSWORD = '1234'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False


SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(days=1)
