#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import BaseQuery
from apps import db


class TagQuery(BaseQuery):

    def getall(self):
        return self.all()

    def gettag_id(self, id):
        return self.get(id)


class Tag(db.Model):
    __tablename__ = 'tag'
    query_class = TagQuery
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    #post = db.relationship('Post', secondary=article_tags)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<tag name %r>' % self.name