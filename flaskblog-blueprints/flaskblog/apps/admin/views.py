#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint,render_template,request,session,redirect,flash,url_for,abort
from apps import app,db
from apps.category.models import Category
from apps.page.models import Post
from apps.tag.models import Tag
from werkzeug import secure_filename
import time
import json
admin = Blueprint('admin',__name__)




@admin.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('admin.newpost'))
    return render_template('login.html')


@admin.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@admin.route('/newpost')
def newpost():
    categories = Category.query.getall()
    return render_template('/newpost.html', categories=categories)


@admin.route('/addpost', methods=['POST'])
def addpost():
    if not session.get('logged_in'):
        abort(401)
    elif request.method == 'POST':
        tagtemp = []
        taglist = request.form['tags'].split(',')
        for i in taglist:
            tagtemp.append(Tag(name=i))

        db.session.add(Post(tags=tagtemp, post_content=request.form['content'], post_title=request.form['title'], category_id=request.form['category'], post_name=request.form['postname'], tags_name=request.form['tags']))
        db.session.commit()
        db.session.commit()

    return redirect(url_for('newpost'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@admin.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('imgFile', None)

        if file and allowed_file(file.filename):
            filename = str(int(time.time())) + '_' + secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            data = {'error': 0, 'url': app.config['UPLOAD_FOLDER'] + filename}
            return json.dumps(data)
    return 'FAIL!'


@admin.route('/epost', methods=['GET'])
def epost():
    num = request.args.get('post', '')
    if num:
        p = Post.query.get_or_404(num)
        return render_template('/editpost.html', p=p)
    return redirect(url_for('error_404'))


@admin.route('/apost', methods=['POST'])
def apost():
    if not session.get('logged_in'):
        abort(401)
    elif request.method == 'POST':
        p = Post.query.getpost_id(request.form['num'])
        p.post_title = request.form['title']
        p.post_name = request.form['postname']
        p.post_content = request.form['content']
        db.session.commit()
    return redirect(url_for('newpost'))