#!/usr/bin/env python
# -*- coding: utf8 -*-

from flask import Blueprint, render_template, jsonify, request
import simplejson as json
import twitter

from myblog import app
from myblog.models.model import Post
from myblog.models.model import Tag

fe = Blueprint('fe', __name__)

@app.errorhandler(404)
def page_not_found(error):
    return "Page not found", 404

@fe.route('/')
@fe.route('/tag/')
@fe.route('/tag/<string:tag>')
def index(tag=None):
    post_list = Post.list(tag=tag).all()
    popular_tags = Tag.list_with_reps("tag_weight DESC", 3).all()
    return render_template('fe/index.html', \
            posts=post_list,\
            popular_tags=popular_tags)

@fe.route('/tags/')
def tags():
    max_weight = 10
    min_weight = 1
    all_tags = Tag.list_with_reps().all()
    popular_tags = Tag.list_with_reps("tag_weight DESC", 3).all()
    return render_template('fe/tags.html', \
            tags=all_tags,\
            popular_tags=popular_tags,
            max_weight=max_weight,\
            min_weight=min_weight)

@fe.route('/_tweets/')
def tweets():
    api = twitter.Api(consumer_key=app.config['TW_CONSUMER_KEY'],\
            consumer_secret=app.config['TW_CONSUMER_SECRET'],\
            access_token_key=app.config['TW_ACCESS_TOKEN_KEY'],\
            access_token_secret=app.config['TW_ACCESS_TOKEN_SECRET']
            )
    dct = [t.AsDict() for t in api.GetUserTimeline()]
    return jsonify(timeline=dct)
