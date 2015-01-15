#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
    manager.py
    ~~~~~~~~~~~

    flask manager script

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.script import Server, Manager, prompt_bool
from myapp import app
from model import db

manager = Manager(app)
manager.add_command("runserver", Server('0.0.0.0', port=5000))


@manager.command
def createall():
    "Creates database tables"
    db.create_all()
    "add Category"
    lists=[u'PYTHON',u'编程珠玑',u'数据库',u'操作系统',u"杂项"]
    from model import Category
    for i in range(1, 6):
        item = Category()
        item.id = i
        item.category_name = lists[i-1]
        db.session.add(item)
    db.session.commit()


@manager.command
def dropall():
    "Drops all database tables"

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

if __name__ == "__main__":
    manager.run()
