# -*- coding:utf-8 -*-
from flask import Flask
from flask import render_template, session, redirect, url_for, request, g, send_from_directory
import config

from functools import wraps
import time
import os
import logging

from models import *
from exts import db
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
with app.app_context():
    db.create_all()
logging.basicConfig(filename="log.txt", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('userid') and session.get('isadmin') == 0:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login_get'))

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('userid') and session.get('isadmin') == 1:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login_get'))

    return wrapper


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('test.html')


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    info_dict = request.form.to_dict()
    print info_dict, 'info_dict'
    print info_dict['username'], 'login'
    user = User.query.filter(User.Username == info_dict['username']).first()
    if user is None:
        print '用户名不存在'
        return render_template('login.html', loginfailed=1)
    if user.confirm_password(info_dict['password']) is not True:
        print '密码错误'
        return render_template('login.html', loginfailed=1)
    else:
        session['userid'] = user.ID
        session['isadmin'] = int(user.IsAdmin)
        session['username'] = user.Username
        session['realname'] = user.RealName
        session['studentID'] = user.StudentNumber
        session['mailbox'] = user.Mail
        print '登录成功 isadmin:', user.IsAdmin, type(user.IsAdmin)
    return redirect(url_for('main'))
    """
    if session['isadmin'] is 0:
        return redirect(url_for('user'))
    else:
        return redirect(url_for('admin'))
    """


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('main'))


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register_post():
    info_dict = request.form.to_dict()
    print info_dict
    print request.form.get('username'), 'register'

    studentid_list = []
    username_list = []
    result = User.query.filter().all()
    for i in result:
        studentid_list.append(i.StudentNumber)
        username_list.append(i.Username)

    if info_dict['studentID'] in studentid_list:
        print '用户学号已存在'
        return render_template('signup.html', signupfailed=1)
    elif info_dict['username'] in username_list:
        print '用户名存在'
        return render_template('signup.html', signupfailed=1)
    else:
        isadmin = 1 if info_dict['studentID'] == '2016110901011' else 0
        user = User(
            IsAdmin=isadmin,
            SignupTime=str(time.time()),
            Username=info_dict['username'],
            Password=generate_password_hash(info_dict['password']),
            RealName=info_dict['realName'],
            StudentNumber=info_dict['studentID'],
            Mail=info_dict['mailbox']
        )
        db.session.add(user)
        if isadmin == 0:
            rank = Rank(
                StudentNumber=info_dict['studentID'],
                Username=info_dict['username']
            )
            db.session.add(rank)
            print u'非管理员注册成功,计入排行榜'
        db.session.commit()
        print info_dict['username'], "注册成功"
        return redirect(url_for('login_get'))


def ranking(username):
    rank_list = Rank.query.filter().order_by(Rank.Score.desc()).all()  # .limit(10).all()
    rank = Rank.query.filter(Rank.Username == username).first()

    t_rank = rank_list.index(rank)
    print 't_rank:', t_rank
    ranking_item = {'ranking': t_rank + 1, 'username': username, 't_score': rank.Score, 'score': []}
    if rank.HardwareBasic != 0:
        ranking_item['score'].append({'direction': u'硬件', 'type': u'基础题', 'score': rank.HardwareBasic})
    if rank.HardwareAdvanced != 0:
        ranking_item['score'].append({'direction': u'硬件', 'type': u'进阶题', 'score': rank.HardwareAdvanced})
    if rank.EmbeddedBasic != 0:
        ranking_item['score'].append({'direction': u'嵌入式', 'type': u'基础题', 'score': rank.EmbeddedBasic})
    if rank.EmbeddedAdvanced != 0:
        ranking_item['score'].append({'direction': u'嵌入式', 'type': u'进阶题', 'score': rank.EmbeddedAdvanced})
    if rank.FrontendBasic != 0:
        ranking_item['score'].append({'direction': u'前端', 'type': u'基础题', 'score': rank.FrontendBasic})
    if rank.FrontendAdvanced != 0:
        ranking_item['score'].append({'direction': u'前端', 'type': u'进阶题', 'score': rank.FrontendAdvanced})
    if rank.DataScienceBasic != 0:
        ranking_item['score'].append({'direction': u'数据科学', 'type': u'基础题', 'score': rank.DataScienceBasic})
    if rank.DataScienceAdvanced != 0:
        ranking_item['score'].append({'direction': u'数据科学', 'type': u'进阶题', 'score': rank.DataScienceAdvanced})
    if rank.OpenQuestion != 0:
        ranking_item['score'].append({'direction': u'开放题', 'type': u'开放题', 'score': rank.OpenQuestion})
    return ranking_item


@app.route('/admin', methods=['GET'])
@admin_required
def admin():
    # total ranking
    rank = [i.Username for i in Rank.query.filter(Rank.Score > 0).order_by(Rank.Score.desc()).all()]
    ranking_list = list()
    for i in rank:
        ranking_list.append(ranking(i))

    # total submit
    submitrecord_list = SubmitRecord.query.filter(SubmitRecord.Confirmed == u'no').all()
    if not submitrecord_list:
        return render_template('admin.html', ranking_list=ranking_list)
    submit_list = [{
        'submitid': i.ID,
        'direction': i.Type.split('_')[0],
        'type': i.Type.split('_')[-1],
        'username': i.Username,
        'realname': i.RealName,
        'message': i.Message,
        'filepath': i.FilePath
    } for i in submitrecord_list]

    return render_template('admin.html', submits=submit_list, ranking_list=ranking_list)


@app.route('/admin', methods=['POST'])
@admin_required
def admin_score():
    info_dict = request.form.to_dict()

    submitrecord = SubmitRecord.query.filter(SubmitRecord.ID == int(info_dict['submitid'])).first()
    submitrecord.Confirmed = 'yes'
    rank = Rank.query.filter(Rank.Username == info_dict['username']).first()
    if info_dict['direction'] == u'硬件':
        if info_dict['type'] == u'基础题':
            rank.HardwareBasic = int(info_dict['score'])
        else:
            rank.HardwareAdvanced = int(info_dict['score'])
    elif info_dict['direction'] == u'嵌入式':
        if info_dict['type'] == u'基础题':
            rank.EmbeddedBasic = int(info_dict['score'])
        else:
            rank.EmbeddedAdvanced = int(info_dict['score'])
    elif info_dict['direction'] == u'前端':
        if info_dict['type'] == u'基础题':
            rank.FrontendBasic = int(info_dict['score'])
        else:
            rank.FrontendAdvanced = int(info_dict['score'])
    elif info_dict['direction'] == u'数据科学':
        if info_dict['type'] == u'基础题':
            rank.DataScienceBasic = int(info_dict['score'])
        else:
            rank.DataScienceAdvanced = int(info_dict['score'])
    else:
        rank.OpenQuestion = int(info_dict['score'])
    rank.Score = rank.HardwareBasic + rank.HardwareAdvanced + \
                 rank.EmbeddedBasic + rank.EmbeddedAdvanced + \
                 rank.FrontendBasic + rank.FrontendAdvanced + \
                 rank.DataScienceBasic + rank.DataScienceAdvanced + \
                 rank.OpenQuestion
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/user', methods=['GET', 'POST'])
@user_required
def user():
    # personal ranking
    ranking_item = ranking(g.username)

    # total ranking
    rank = [i.Username for i in Rank.query.filter(Rank.Score > 0).order_by(Rank.Score.desc()).all()]
    ranking_list = list()
    for i in rank:
        ranking_list.append(ranking(i))
    return render_template('user.html', ranking_item=ranking_item, ranking_list=ranking_list)


@app.route('/user/submit', methods=['GET'])
@user_required
def submit_get():
    return render_template('submit.html')


@app.route('/user/submit', methods=['POST'])
@user_required
def submit_post():
    app.logger.info('submitpost')
    info_dict = request.form.to_dict()
    print info_dict
    f = request.files.get('file1')
    if f:
        print 'f.filename:', f.filename, type(f.filename), type(f)
        suffix = f.filename.split('.')[-1].encode('utf-8')
        file_path = '{}_{}.{}'.format(
            g.studentID,
            time.strftime("%m%d-%H%M", time.localtime(time.time())),
            suffix
        )
        f.save('static/uploads/'+file_path)
    else:
        file_path = ''
    print 'file_path:', file_path

    submitrecord = SubmitRecord(Time=time.time(),
                                Confirmed='no',
                                Username=g.username,
                                RealName=g.realname,
                                Type=info_dict['selected'],
                                FilePath=file_path,
                                Message=info_dict['comments'])
    db.session.add(submitrecord)
    db.session.commit()

    return render_template('submit.html')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    return render_template('basic.html')


@app.route('/static/uploads/<filename>', methods=['GET'])
def download(filename):
    directory = os.getcwd() + '/static/uploads/'
    print 'directory:', directory
    return send_from_directory(directory, filename, as_attachment=True)


@app.before_request
def my_before_request():
    userid = session.get('userid')
    if userid:
        g.userid = userid
        g.isadmin = session.get('isadmin')
        g.studentID = session.get('studentID')
        g.username = session.get('username').encode('utf-8')
        g.realname = session.get('realname').encode('utf-8')
        g.mailbox = session.get('mailbox')
        app.logger.info(g.username, u"已登录")
    else:
        app.logger.info(u"未登录")


@app.context_processor
def my_context_processor():
    userid = session.get('userid')
    if userid:
        username = session.get('username')
        studentID = session.get('studentID')
        mailbox = session.get('mailbox')
        app.logger.info("context_processor:username=%s" % username)
        return {'username': username,
                'studentID': studentID,
                'mailbox': mailbox}
    return {}


if __name__ == '__main__':
    app.run(debug=True)
