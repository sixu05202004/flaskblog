#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import url_for
from flask.ext.sqlalchemy import BaseQuery
from apps.tag.models import Tag
from apps.category.models import Category

from apps import db
from datetime import datetime
from werkzeug import cached_property

article_tags = db.Table('tags',
                        db.Column(
                            'tag_id', db.Integer, db.ForeignKey('tag.id')),
                        db.Column(
                            'post_id', db.Integer, db.ForeignKey('post.id')),
                        )


class PostQuery(BaseQuery):

    def getpost_id(self, id):
        return self.get(id)

    def getall(self):
        return self.all()

    def getpost_byname(self, name):
        return self.filter(Post.post_name.ilike(name)).distinct().first()

    def getpost_perpage(self, pageid, per_page):
        return self.order_by(Post.post_create_time.desc()).paginate(pageid, per_page)

    def hottest(self):
        return self.order_by(Post.comment_count.desc(), Post.view_num.desc())

    def newpost(self):
        return self.order_by(Post.post_modified_time.desc())

    def search(self, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(Post.post_title.ilike(keyword),
                                   Post.post_content.ilike(keyword),
                                   Post.tags_name.ilike(keyword)))

        q = reduce(db.and_, criteria)

        return self.filter(q).distinct()

    def search_tag(self, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(Post.tags_name.ilike(keyword)))

        q = reduce(db.and_, criteria)

        return self.filter(q).distinct()


class Post(db.Model):
    __tablename__ = 'post'
    query_class = PostQuery
    id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.Text)
    post_title = db.Column(db.String(100))
    post_name = db.Column(db.String(200), unique=True)
    post_create_time = db.Column(db.DateTime, default=datetime.utcnow)
    view_num = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=1)
    author_id = db.Column(db.Integer, default=1)
    post_modified_time = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    categorys = db.relationship('Category', backref=db.backref(
        'posts', lazy='dynamic'), lazy='select')
    tags = db.relationship('Tag', secondary=article_tags,
                           backref=db.backref('posts', lazy='dynamic'))
    tags_name = db.Column(db.Text)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<post %r>' % self.post_title
    
    @cached_property
    def comments(self):
        from apps.comment.models import Comment
        allcomments = Comment.query.filter(Comment.post_id == self.id).all()
        return allcomments
    
def pageby(obj, pageid, per_page, orderby):
    return obj.order_by(orderby).paginate(pageid, per_page)
