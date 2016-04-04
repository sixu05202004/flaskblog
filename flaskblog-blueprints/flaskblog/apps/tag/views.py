#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint,render_template
from apps import app,cache
from apps.category.models import Category
from apps.page.models import Post,pageby
from apps.tag.models import Tag
from apps.comment.models import Comment
from random import shuffle
tag = Blueprint('tag',__name__)
per_page = app.config['PER_PAGE']





@tag.route('/<int:tagid>')
@tag.route('/<int:tagid>/page/<int:pageid>')
@cache.cached(timeout=300)
def tag_1(tagid=1, pageid=1):
    categorys = Category.query.getall()
    hot = Post.query.hottest()[:20]
    new = Post.query.newpost()[:20]
    tag = Tag.query.getall()
    shuffle(tag)
    tag = tag[:20]
    comments = Comment.query.newcomment()[:20]

    tagall = Tag.query.get_or_404(tagid)
    name = tagall.name
    p = Post.query.search_tag(name)
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