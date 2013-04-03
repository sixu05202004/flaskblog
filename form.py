# -*- coding: utf-8 -*-
"""
    form.py
    ~~~~~~~~~~~

    comment form

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form, SubmitField, TextField, required, length, TextAreaField, email, RecaptchaField, HiddenField


class CommentForm(Form):
    author_name = TextField(u'Name', validators=[required(message=u"Need an name"), length(max=50)])
    author_email = TextField(u"Email", validators=[
                             required(message=u"Need an email address"),
                             email(message=u"Need a valid email address")])
    author_url = TextField(u"Url")
    content = TextAreaField(u"Content")
    post_id = TextField()
    recaptcha = RecaptchaField(u"Copy the words appearing below")
    submit = SubmitField(u"Save")
