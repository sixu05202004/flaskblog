# -*- coding: utf-8 -*-

"""
    setup.py
    ~~~~~~~~~~~

    set up extensions

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from setuptools import setup

setup(
    install_requires=[
        'Flask',
        'Flask-Cache',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-Testing',
        'Flask-Script',
        'Flask-Uploads',
        'sqlalchemy'
    ]

)