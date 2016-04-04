#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
    form.py
    ~~~~~~~~~~~

    comment form

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form, RecaptchaField
from wtforms import SubmitField, TextField, TextAreaField
from wtforms.validators import InputRequired, Email,  Length


class CommentForm(Form):
    author_name = TextField(
        u'Name', validators=[InputRequired(message=u"Need an name"), Length(max=50)])
    author_email = TextField(u"Email", validators=[
                             InputRequired(message=u"Need an email address"),
                             Email(message=u"Need a valid email address")])
    author_url = TextField(u"Url")
    content = TextAreaField(u"Content")
    post_id = TextField()
    recaptcha = RecaptchaField(u"Copy the words appearing below")
    submit = SubmitField(u"Save")
