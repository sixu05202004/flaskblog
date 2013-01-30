# -*- coding: utf-8 -*-
from flask import url_for,g
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from werkzeug import cached_property
from datetime import datetime
from myapp import app

db = SQLAlchemy(app)


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

    def __init__(self, category_name):
        self.category_name = category_name

    def __repr__(self):
        return '<category name %r>' % self.category_name


article_tags = db.Table('tags',
                        db.Column(
                            'tag_id', db.Integer, db.ForeignKey('tag.id')),
                        db.Column(
                            'post_id', db.Integer, db.ForeignKey('post.id')),
                        )


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

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<tag name %r>' % self.name


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
        return self.order_by(Post.post_create_time.desc())

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
    def __init__(self, tags, post_content, post_title, category_id,  post_name, 
                 tags_name, post_create_time=None, view_num=0, comment_count=0, status=1,
                 author_id=1, post_modified_time=None):
        self.post_content = post_content
        self.post_title = post_title
        self.category_id = category_id
        self.post_name = post_name
        if post_create_time is None:
            self.post_create_time = datetime.utcnow()
        self.view_num = view_num
        self.comment_count = comment_count
        self.status = status
        self.author_id = author_id
        if post_modified_time is None:
            self.post_modified_time = post_modified_time
        #self.categorys = category
        self.tags = tags
        self.tags_name = tags_name

    def __repr__(self):
        return '<post %r>' % self.post_title

    def _url(self):
        return url_for('post', name=self.post_name)

    @cached_property
    def url(self):
        return self._url()

    @cached_property
    def comments(self):
        allcomments = Comment.query.filter(Comment.post_id == self.id).all()
        return allcomments


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
    author = db.Column(db.String(50))
    author_email = db.Column(db.String(100))
    author_url = db.Column(db.String(1024))
    author_ip = db.Column(db.String(20))
    comment_create_time = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)
    isvisible = db.Column(db.Integer, default=1)

    def __init__(self, postid, author, author_email, author_url, author_ip,
                 content, isvisible=1, comment_create_time=None):
        self.post_id = postid
        self.author = author
        self.author_email = author_email
        self.author_url = author_url
        self.author_ip = author_ip
        self.content = content
        self.isvisible = isvisible
        if comment_create_time is None:
            self.comment_create_time = datetime.utcnow()

    def __repr__(self):
        return '<comment %r>' % self.content

def pageby(obj, pageid, per_page, orderby):
    return obj.order_by(orderby).paginate(pageid, per_page)

if __name__ == '__main__':
    
    #print Post.query.search('7998797').order_by(Post.post_create_time.desc()).paginate(1, 10).items
    #print len(Tag.query.getall())
    #print p.total
    #db.create_ll()
    #a=Category("test")
    #db.session.add(a)
    #print app.config['PER_PAGE']
    #print Tag.query.gettag_id(2).posts.all()
    #print Post.query.getpost_id(54).comments.all()
    #print Category.query.getcategory_id(3).posts.order_by(Post.post_create_time.desc()).paginate(1, 10).items


    #p=Post.query.getpost_id(110)
    #print Post.query.search_tag(Tag.query.gettag_id(1).name).all()
    print Tag.query.gettag_id(1).name
    """
    a=Category("test2")
    b1=Tag('3')
    b2=Tag('4')
    c=Post(a,[b1,b2],'000','0','a')
    db.session.add(a)
    db.session.add(b1)
    db.session.add(b2)
    db.session.add(c)
    db.session.commit()
    """
    #c = Comment(1458,'dan','dan@izptec.com','www.baidu.com','10.0.11.111','不错')
    #db.session.add(c)
    #db.session.commit()

    #print db.engine.execute('update post set comment_count = comment_count + 1 where id = 1458')
    #print c.tags[0].name
    #print db