# -*- coding: utf-8 -*-

# configuration page num 
PER_PAGE = 10

# configuration mysql

SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s"%('admin','admin','127.0.0.1','test')

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
USERNAME = 'admin'
PASSWORD = 'admin'

UPLOAD_FOLDER = '/static/upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])