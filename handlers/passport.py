# -*- coding: utf-8 -*-
# @Time    : 20-4-13 下午4:40
# @File    : handlers.py
import logging

from basehandler import BaseHandler


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write('hi')


class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        logging.debug("debug msg")
        logging.info("info msg")
        logging.warning("warning msg")
        logging.error("error msg")
        self.write('login')