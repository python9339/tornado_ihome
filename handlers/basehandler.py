# -*- coding: utf-8 -*-
# @Time    : 20-4-13 下午4:28
# @File    : baseHandler.py

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def set_default_headers(self):
        pass

    def initialize(self):
        pass

    def prepare(self):
        pass

    def write_error(self, status_code, **kwargs):
        pass

    def on_finish(self):
        pass