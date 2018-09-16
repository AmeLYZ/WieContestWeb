# -*- coding:utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from index import app

from models import *
from exts import db
import time

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def add_user():
    admin = User(IsAdmin='1',
                 SignupTime=str(time.time()),
                 Username='ame',
                 Password=generate_password_hash('123'),
                 RealName='刘雨瓒',
                 StudentNumber='2016110901011',
                 Mail='532071027@qq.com')
    db.session.add(admin)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
