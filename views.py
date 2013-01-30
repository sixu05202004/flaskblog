# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect, request, flash, session
from myapp import app
from model import article_tags, Category, Post, Tag, Comment, pageby, db
from werkzeug import secure_filename
from flask.ext.cache import Cache
from random import shuffle
from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
import os
import json
import time

cache = Cache(app)
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


def is_chinese(text):
    if text:
        for uchar in text:
            if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
                return True
    return False


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/error/404')
def error_404():
    return render_template('404.html'), 404


@app.route('/')
@app.route('/page/<int:pageid>')
@cache.cached(timeout=300)
def index(pageid=1):

    categorys = Category.query.getall()

    p = Post.query.getpost_perpage(pageid, per_page)
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]

    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]

    comments = Comment.query.newcomment()[:20]
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
@cache.cached(timeout=300)
def about():
    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]

    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]

    comments = Comment.query.newcomment()[:20]

    return render_template('/about.html',
                           categorys=categorys,
                           hotarticles=hot,
                           newpost=new,
                           tags=tag,
                           comments=comments)


@app.route('/category/<int:cateid>')
@app.route('/category/<int:cateid>/page/<int:pageid>')
@cache.cached(timeout=300)
def category(cateid=1, pageid=1):
    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]
    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]
    comments = Comment.query.newcomment()[:20]

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
@cache.cached(timeout=300)
def tag(tagid=1, pageid=1):
    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]
    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]
    comments = Comment.query.newcomment()[:20]


    tagall = Tag.query.gettag_id(tagid)
    if not tagall:
        return redirect(url_for('error_404'))

    p = Post.query.search_tag(Tag.query.gettag_id(tagid).name)
    p = pageby(p, pageid, per_page, Post.post_create_time.desc())

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
@cache.cached(timeout=240)
def search(pageid=1):

    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]
    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]
    comments = Comment.query.newcomment()[:20]

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
                           key=searchword,
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
@cache.cached(timeout=300)
def article(postid=5):
    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]
    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]
    comments = Comment.query.newcomment()[:20]
    articles = Post.query.getall()
    shuffle(articles)
    articles = articles[:5]

    post = Post.query.getpost_id(postid)

    if not post:
        return redirect(url_for('error_404'))
    postcoments = post.comments.all()
    post.view_num += 1
    db.session.commit()
    return render_template('/post.html',
                           post=post,
                           articles=articles,
                           categorys=categorys,
                           hotarticles=hot,
                           newpost=new,
                           tags=tag,
                           comments=comments,
                           postcoments=postcoments
                           )


@app.route('/<postname>.html')
@cache.cached(timeout=300)
def article_byname(postname):
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

    post = Post.query.getpost_byname(postname)

    if not post:
        return redirect(url_for('error_404'))
    postcoments = post.comments.all()
    post.view_num += 1
    db.session.commit()

    return render_template('/post.html',
                           post=post,
                           articles=articles,
                           categorys=categorys,
                           hotarticles=hot,
                           newpost=new,
                           tags=tag,
                           comments=comments,
                           postcoments=postcoments
                           )


@app.route('/addcomment', methods=['POST'])
def addcomment():
    error = 'POST not legal!!!!'
    if request.method == 'POST' and 'pythonpub.com' in \
            request.environ.get('HTTP_REFERER'):
        if not request.form.get('author') or \
                len(request.form.get('author')) >= 51:
            error = u'请填写必填项目（姓名和电子邮件地址）或者确保长度在规定范围内或者格式正确'
        elif not request.form.get('email') or \
                '@' not in request.form.get('email') or \
                len(request.form.get('email')) >= 101:
            error = u'请填写必填项目（姓名和电子邮件地址）或者确保长度在规定范围内或者格式正确'
        elif len(request.form.get('url')) >= 1025:
            error = u'网址过长'
        elif not request.form.get('comment') or not is_chinese(request.form.get('comment')):
            error = u'评论为空或者评论中无中文汉字'
        elif request.environ.get('HTTP_X_FORWARDED_FOR') and request.form.get('nonce') and len(request.form.get('nonce')) in [1,2,3,4]:
            c = Comment(request.form['comment_post_ID'], request.form['author'], request.form['email'], request.form['url'],
                        request.environ['HTTP_X_FORWARDED_FOR'], request.form['comment'])
            db.session.add(c)
            post = Post.query.getpost_id(request.form['comment_post_ID'])
            post.comment_count += 1
            db.session.commit()
            #db.engine.execute('update post set comment_count = comment_count \
            #                    + 1 where id =' + request.form['comment_post_ID'])
            #flash('You were successfully commented!')
            return redirect(url_for('article', postid=request.form['comment_post_ID']))

    return render_template('/error.html', content=error)


@app.route('/error')
def error(content='404'):
    return render_template('/error.html', content=content)


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
        tagtemp = []
        taglist = request.form['tags'].split(',')
        for i in taglist:
            tagtemp.append(Tag(i))

        db.session.add(Post(tagtemp, request.form['content'], request.form['title'], request.form['category'], request.form['postname'], request.form['tags']))
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
            file.save('/home/pythonspace/webapps/pythonpub/htdocs/myblog' + app.config['UPLOAD_FOLDER'] + filename)
            data = {'error': 0, 'url': app.config['UPLOAD_FOLDER'] + filename}
            return json.dumps(data)
    return 'FAIL!'

@app.route('/epost', methods=['GET'])
def epost():
  num = request.args.get('post','')
  if num:
    p=Post.query.getpost_id(num)
    return render_template('/editpost.html', p=p)
  return redirect(url_for('error_404'))

@app.route('/apost', methods=['POST'])
def apost():
    if not session.get('logged_in'):
        abort(401)
    elif request.method == 'POST':
        p=Post.query.getpost_id(request.form['num'])
        p.post_title = request.form['title']
        p.post_name = request.form['postname']
        p.post_content = request.form['content']
        db.session.commit()
    return redirect(url_for('newpost'))
