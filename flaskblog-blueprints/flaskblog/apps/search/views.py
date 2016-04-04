#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Blueprint,render_template,request,redirect,url_for
from apps import app,cache
from apps.category.models import Category
from apps.page.models import Post,pageby
from apps.tag.models import Tag
from apps.comment.models import Comment
from random import shuffle
search = Blueprint('search',__name__)
per_page = app.config['PER_PAGE']


@app.route('/search')
@app.route('/search/page/<int:pageid>')
@cache.cached(timeout=240)
def search_1(pageid=1):

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