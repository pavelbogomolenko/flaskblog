#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.sql import extract
from flask.ext.sqlalchemy import SQLAlchemy
from myblog import app

db = SQLAlchemy(app)

# association MM table
post_tags = db.Table('post_tags', db.Model.metadata,\
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),\
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    tags = db.relationship('Tag', secondary=post_tags, backref='posts')

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.pub_date = datetime.utcnow()

    def __repr__(self):
        s = [(a, getattr(self, str(a))) for a in self.__dict__.keys() if not a.startswith('_')]
        return repr(s)

    def __unicode__(self):
        return self.title

    @staticmethod
    def list(**kvargs):
        base = Post.query
        if 'year' in kvargs:
            year = kvargs['year']
            if year:
                base = base.filter(extract('year', Post.pub_date) == year)
        elif 'tag' in kvargs:
            tag = kvargs['tag']
            if tag:
                base = base.filter(Post.tags.any(title = tag))
        base = base.order_by(Post.pub_date.desc())
        return base

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        s = [(a, getattr(self, str(a))) for a in self.__dict__.keys() if not a.startswith('_')]
        return repr(s)

    def __unicode__(self):
        return self.title
    @staticmethod
    def list_with_reps(order="tags.title", limit=None):
        count_tags_query = db.session.query(func.count(post_tags.columns.get("tag_id"))).\
                filter(post_tags.columns.get("tag_id") == Tag.id).label("tag_weight")
        tags_with_count_query = db.session.query(Tag, count_tags_query).order_by(order).limit(limit)
        return tags_with_count_query
