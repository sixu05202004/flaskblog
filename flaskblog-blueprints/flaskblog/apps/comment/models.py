#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import BaseQuery
from apps.page.models import Post
from apps import db
from datetime import datetime

class CommentQuery(BaseQuery):

    def getall(self):
        return self.all()

    def getcomment_id(self, id):
        return self.get(id)

    def newcomment(self):
        return self.order_by(Comment.comment_create_time.desc())


class Comment(db.Model):
    __tablename__ = 'comment'
    query_class = CommentQuery
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    posts = db.relationship('Post', backref=db.backref('comments', lazy='dynamic'))
    author_name = db.Column(db.String(50))
    author_email = db.Column(db.String(100))
    author_url = db.Column(db.String(1024))
    author_ip = db.Column(db.String(20))
    comment_create_time = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)
    isvisible = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<comment %r>' % self.content