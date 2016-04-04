#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
from werkzeug.contrib.atom import AtomFeed
from apps import app, cache
from apps.category.models import Category
from apps.page.models import Post
from apps.tag.models import Tag
from apps.comment.models import Comment
from random import shuffle
from datetime import datetime
index = Blueprint('index', __name__)
per_page = app.config['PER_PAGE']


class PostFeed(AtomFeed):

    def add_post(self, post):

        self.add(post.post_title,
                 '',
                 content_type="html",
                 author=u'dan',
                 url=post.url,
                 updated=datetime.now(),
                 published=post.post_create_time)


@index.route('/')
@index.route('page/<int:pageid>')
@cache.cached(timeout=300)
def index_1(pageid=1):
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


@index.route('/rss_lastnews')
@cache.cached(timeout=86400)
def rss_lastnews():
    feed = PostFeed("pythonpub - lastnews",
                    feed_url=request.url,
                    url=request.url_root)
    new = Post.query.newpost().limit(15)
    for post in new:
        feed.add_post(post)

    return feed.get_response()
