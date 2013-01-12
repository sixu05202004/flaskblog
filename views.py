# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect, request, flash, session
from myapp import app
from model import article_tags, Category, Post, Tag, Comment, pageby, db
from werkzeug import secure_filename
from random import shuffle
from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
import os
import json
import time
app.config.from_object('config')
per_page = app.config['PER_PAGE']


class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


def html2textile(html):
    return dehtml(html)

app.jinja_env.filters['html2textile'] = html2textile






@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/error/404')
def error_404():
    return render_template('404.html'), 404


@app.route('/')
@app.route('/page/<int:pageid>')
def index(pageid=1):

    categorys = Category.query.getall()

    p = Post.query.getpost_perpage(pageid, per_page)
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]

    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]

    comments = Comment.query.getall()[:20]
    articles = p.items
    if not p.total:
        pagination = [0]
    elif p.total % per_page:
        pagination = range(1, p.total / per_page + 2)
    else:
        pagination = range(1, p.total / per_page + 1)

    return render_template('/index.html',
                           categorys=categorys,
                           articles=articles,
                           hotarticles=hot,
                           newpost=new,
                           tags=tag,
                           comments=comments,
                           pageid=pageid,
                           pagination=pagination[pageid - 1:pageid + 10],
                           last_page=pagination[-1],
                           nav_current="index"
                           )


@app.route('/about')
def about():
    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]

    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]

    comments = Comment.query.getall()[:20]
    return render_template('/about.html',
                           categorys=categorys,
                           hotarticles=hot,
                           newpost=new,
                           tags=tag,
                           comments=comments)


@app.route('/category/<int:cateid>')
@app.route('/category/<int:cateid>/page/<int:pageid>')
def category(cateid=1, pageid=1):
    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]
    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]
    comments = Comment.query.getall()[:20]

    cate = Category.query.getcategory_id(cateid)
    if not cate:
        return redirect(url_for('error_404'))

    p = pageby(cate.posts, pageid, per_page, Post.post_create_time.desc())

    articles = p.items
    if not p.total:
        pagination = [0]
    elif p.total % per_page:
        pagination = range(1, p.total / per_page + 2)
    else:
        pagination = range(1, p.total / per_page + 1)

    return render_template('/category.html',
                           id=cateid,
                           cate=cate,
                           categorys=categorys,
                           articles=articles,
                           hotarticles=hot,
                           newpost=new,
                           tags=tag,
                           comments=comments,
                           pageid=pageid,
                           pagination=pagination[pageid - 1:pageid + 10],
                           last_page=pagination[-1]
                           )

@app.route('/tag/<int:tagid>')
@app.route('/tag/<int:tagid>/page/<int:pageid>')
def tag(tagid=1, pageid=1):
    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]
    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]
    comments = Comment.query.getall()[:20]

    tagall = Tag.query.gettag_id(tagid)
    if not tagall:
        return redirect(url_for('error_404'))

    p = pageby(tagall.posts, pageid, per_page, Post.post_create_time.desc())

    articles = p.items
    if not p.total:
        pagination = [0]
    elif p.total % per_page:
        pagination = range(1, p.total / per_page + 2)
    else:
        pagination = range(1, p.total / per_page + 1)

    return render_template('/tag.html',
                           id=tagid,
                           tagall=tagall,
                           categorys=categorys,
                           articles=articles,
                           hotarticles=hot,
                           newpost=new,
                           tags=tag,
                           comments=comments,
                           pageid=pageid,
                           pagination=pagination[pageid - 1:pageid + 10],
                           last_page=pagination[-1]
                           )

@app.route('/search')
@app.route('/search/page/<int:pageid>')
def search(pageid=1):

    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]
    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]
    comments = Comment.query.getall()[:20]

    searchword = request.args.get('s', '')
    if not searchword:
        return redirect(url_for('error_404'))

    searchresult = Post.query.search(searchword)

    p = pageby(searchresult, pageid, per_page, Post.post_create_time.desc())

    articles = p.items
    if not p.total:
        pagination = [0]
    elif p.total % per_page:
        pagination = range(1, p.total / per_page + 2)
    else:
        pagination = range(1, p.total / per_page + 1)

    return render_template('/search.html',
                           key = searchword,
                           categorys=categorys,
                           articles=articles,
                           hotarticles=hot,
                           newpost=new,
                           tags=tag,
                           comments=comments,
                           pageid=pageid,
                           pagination=pagination[pageid - 1:pageid + 10],
                           last_page=pagination[-1]
                           )


@app.route('/article/<int:postid>')
def article(postid=5):
    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]
    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]
    comments = Comment.query.getall()[:20]
    articles = Post.query.getall()
    shuffle(articles)
    articles = articles[:5]

    post = Post.query.getpost_id(postid)
    

    if not post:
        return redirect(url_for('error_404'))
    postcoments = post.comments.all()
    db.engine.execute('update post set view_num = view_num + 1 where id =' + str(postid))
    return render_template('/post.html',
                           post = post,
                           articles = articles,
                           categorys=categorys,
                           hotarticles=hot,
                           newpost=new,
                           tags=tag,
                           comments=comments,
                           postcoments = postcoments
                           )

@app.route('/addcomment', methods=['POST'])
def addcomment():
    if request.method == 'POST':
        if not request.form['author'] or len(request.form['author'])>=51:
            error = u'请填写必填项目（姓名和电子邮件地址）或者确保长度在规定范围内或者格式正确'
        elif not request.form['email'] or \
                 '@' not in request.form['email'] or len(request.form['email'])>=101 :
            error = u'请填写必填项目（姓名和电子邮件地址）或者确保长度在规定范围内或者格式正确'
        elif len(request.form['url'])>=1025:
            error = u'网址过长'
        else:
            c = Comment(request.form['comment_post_ID'], request.form['author'], request.form['email'], request.form['url'],
                        request.environ['REMOTE_ADDR'], request.form['comment'])
            db.session.add(c)
            db.session.commit()
            db.engine.execute('update post set comment_count = comment_count + 1 where id =' + request.form['comment_post_ID'])
            flash('You were successfully commented!')
            return redirect(url_for('article', postid=request.form['comment_post_ID']))

    return render_template('/error.html',content=error)

@app.route('/error')
def error(content='404'):
    return render_template('/error.html',content=content)


@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('newpost'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/newpost')
def newpost():
    categories = Category.query.getall()
    return render_template('/newpost.html', categories=categories)

@app.route('/addpost', methods=['POST'])
def addpost():
    if not session.get('logged_in'):
        abort(401)
    elif request.method == 'POST':
        tagtemp=[]
        taglist = request.form['tags'].split(',')
        for i in taglist:
            tagtemp.append(Tag(i))

        db.session.add(Post(tagtemp, request.form['content'], request.form['title'], request.form['category']))
        db.session.commit() 

    return redirect(url_for('newpost'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('imgFile', None)

        if file and allowed_file(file.filename):
            filename = str(int(time.time())) + '_' + secure_filename(file.filename)
            file.save(os.getcwd()+app.config['UPLOAD_FOLDER']+filename)
            data = {'error':0, 'url':app.config['UPLOAD_FOLDER']+filename}
            return json.dumps(data)
    return 'FAIL!'





