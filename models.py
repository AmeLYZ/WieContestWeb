# -*- coding:utf-8 -*-

from exts import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """
    ID: 用户标识符
    Isadmin: 管理员标识
    SignupTime: 注册时间
    Username: 用户名
    Password: 密码
    RealName: 真实姓名
    StudentNumber: 学号
    Mail: 邮箱
    """
    __tablename__ = 'user'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IsAdmin = db.Column(db.String(20), nullable=False)
    SignupTime = db.Column(db.String(20), nullable=False)
    Username = db.Column(db.String(150), nullable=False)
    Password = db.Column(db.String(150), nullable=False)
    RealName = db.Column(db.String(150), nullable=False)
    StudentNumber = db.Column(db.String(13), nullable=False)
    Mail = db.Column(db.String(150), nullable=False)

    @property
    def password(self):
        raise AttributeError('password cannot be read')

    @password.setter
    def password(self, password):
        self.Password = generate_password_hash(password)

    def confirm_password(self, password):
        return check_password_hash(self.Password, password)


class SubmitRecord(db.Model):
    """
    ID: 提交编号
    Time: 提交时间
    Confirmed: 是否评分
    Username: 提交人用户名
    RealName: 提交人真实姓名
    Type: 题目方向
    FilePath: 文件路径
    Message: 留言
    """
    __tablename__ = 'submitrecord'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Time = db.Column(db.String(20), nullable=False)
    Confirmed = db.Column(db.String(20), nullable=False)
    Username = db.Column(db.String(150), nullable=False)
    RealName = db.Column(db.String(150), nullable=False)
    Type = db.Column(db.String(150), nullable=False)
    FilePath = db.Column(db.String(150), nullable=False)
    Message = db.Column(db.String(350), nullable=False)


class Rank(db.Model):
    """
    ID: 标识符
    StudentNumber: 学号
    Username: 用户名
    Score: 总得分
    HardwareBasic: 硬件基础题得分
    HardwareAdvanced: 硬件进阶题得分
    EmbeddedBasic: 嵌入式基础题得分
    EmbeddedAdvanced: 嵌入式进阶题得分
    FrontendBasic: 前端基础题得分得分
    FrontendAdvanced: 前端进阶题得分
    DataScienceBasic: 数据科学基础题得分
    DataScienceAdvanced: 数据科学进阶题得分
    OpenQuestion: 开放题得分

    """
    __tablename__ = 'rank'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentNumber = db.Column(db.String(13), nullable=False)
    Username = db.Column(db.String(150), nullable=False)
    Score = db.Column(db.Integer, nullable=False, default=0)
    HardwareBasic = db.Column(db.Integer, nullable=False, default=0)
    HardwareAdvanced = db.Column(db.Integer, nullable=False, default=0)
    EmbeddedBasic = db.Column(db.Integer, nullable=False, default=0)
    EmbeddedAdvanced = db.Column(db.Integer, nullable=False, default=0)
    FrontendBasic = db.Column(db.Integer, nullable=False, default=0)
    FrontendAdvanced = db.Column(db.Integer, nullable=False, default=0)
    DataScienceBasic = db.Column(db.Integer, nullable=False, default=0)
    DataScienceAdvanced = db.Column(db.Integer, nullable=False, default=0)
    OpenQuestion = db.Column(db.Integer, nullable=False, default=0)
