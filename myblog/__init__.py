#!/usr/bin/env python
# -*- coding: utf8 -*-

from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

from myblog.apps.fe.controller import fe
from myblog.apps.be.controller import be

app.register_blueprint(fe)
app.register_blueprint(be)
