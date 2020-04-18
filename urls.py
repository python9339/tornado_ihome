# -*- coding: utf-8 -*-
# @Time    : 20-4-13 下午3:45
# @File    : urls.py
import os

from handlers import passport
from tornado.web import StaticFileHandler

handlers = [
    (r'/login',passport.LoginHandler),
    (r'/(.*)', StaticFileHandler, {'path':os.path.join(os.path.dirname(__file__), "html"), "default_filename":"index.html"})
]