#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint,render_template
from apps import cache
from apps.page.models import Post
from apps.category.models import Category
from apps.tag.models import Tag
from apps.comment.models import Comment
from random import shuffle
about = Blueprint('about',__name__)

@about.route('/')
@cache.cached(timeout=300)
def about_1():
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