#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import BaseQuery
from apps import db


class CategoryQuery(BaseQuery):

    def getall(self):
        return self.all()

    def getcategory_id(self, id):
        return self.get(id)


class Category(db.Model):
    __tablename__ = 'category'
    query_class = CategoryQuery
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(200), unique=True)

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<category name %r>' % self.category_name
