#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Blueprint, render_template, url_for, redirect, request
from apps import cache, db
from apps.category.models import Category
from apps.page.models import Post
from apps.tag.models import Tag
from apps.comment.models import Comment
from apps.comment.forms import CommentForm
from random import shuffle
article = Blueprint('article', __name__)


@article.route('/<int:postid>')
@cache.cached(timeout=300)
def article_1(postid=5):
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

    post = Post.query.get_or_404(postid)
    form = CommentForm()
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
                           postcoments=postcoments,
                           form=form
                           )


@article.route('/addcomment', methods=['POST'])
def addcomment():
    form = CommentForm()
    error = 'Sorry, Post Comments Error!'

    if form.validate_on_submit():
        author_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or '127.0.0.1'
        comment = Comment(author_ip=author_ip)
        form.populate_obj(comment)
        db.session.add(comment)
        post = Post.query.getpost_id(comment.post_id)
        post.comment_count += 1
        db.session.commit()
        return redirect(url_for('article', postid=comment.post_id))

    return render_template('/error.html', content=error)
