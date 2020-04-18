# -*- coding: utf-8 -*-
# @Time    : 20-4-13 下午3:43
# @File    : server.py

import tornado.ioloop
import tornado.httpserver
import tornado.options


from tornado.options import define,options
from application import Application
from urls import handlers
import config

define('port', type=int, default=8000, help="run server on the given port")


if __name__ == '__main__':
    options.logging = config.log_level
    options.log_file_prefix = config.log_file
    tornado.options.parse_command_line()

    app = Application(handlers=handlers, **config.settings)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    # 多进程方式
    # server.bind(options)
    # server.start(0)

    tornado.ioloop.IOLoop.current().start()