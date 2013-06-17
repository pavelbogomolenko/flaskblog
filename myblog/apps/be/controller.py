#!/usr/bin/env python
# -*- coding: utf8 -*-

from flask import Blueprint

from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

from myblog import app
from myblog.models.model import db
from myblog.models.model import Post
from myblog.models.model import Tag

be = Blueprint('be', __name__)

@be.route('/admin')
def admin():
    pass

class PostAdminView(ModelView):
    column_exclude_list = ['text']

    def __init__(self, session):
        super(PostAdminView, self).__init__(Post, session)

admin = Admin(app)
admin.add_view(PostAdminView(db.session))
admin.add_view(ModelView(Tag, db.session))
