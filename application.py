# -*- coding: utf-8 -*-
# @Time    : 20-4-13 下午4:51
# @File    : application.py

import tornado.web
import torndb
import redis

from config import redis_options, mysql_options

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application,self).__init__(*args, **kwargs)

        # self.db = torndb.Connection(
        #     host = mysql_options['host'],
        #     user = mysql_options['user'],
        #     password = mysql_options['password'],
        #     database = mysql_options['database']
        # )
        self.db = torndb.Connection(**mysql_options)

        # self.redis = redis.StrictRedis(
        #     host = redis_options['host'],
        #     port = redis_options['port']
        # )
        self.redis = redis.StrictRedis(**redis_options)