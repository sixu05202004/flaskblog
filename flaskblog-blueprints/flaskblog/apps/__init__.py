#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from HTMLParser import HTMLParser
from re import sub
from traceback import print_exc

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
cache = Cache(app)


from apps.about.views import about
app.register_blueprint(about,url_prefix='/about')
from apps.admin.views import admin
app.register_blueprint(admin,url_prefix='/admin')
from apps.category.views import category
app.register_blueprint(category,url_prefix='/category')
from apps.tag.views import tag
app.register_blueprint(tag,url_prefix='/tag')
from apps.search.views import search
app.register_blueprint(search,url_prefix='/search')
from apps.article.views import article
app.register_blueprint(article,url_prefix='/article')
from apps.index.views import index
app.register_blueprint(index,url_prefix='/')

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


@app.route('/404')
def error_404():
    return render_template('404.html'), 404


@app.route('/error')
def error_temp(content='404'):
    return render_template('error.html', content=content)
