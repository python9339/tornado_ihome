# -*- coding: utf-8 -*-
# @Time    : 20-4-13 下午4:09
# @File    : config.py
import os

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    # template_path=os.path.join(os.path.dirname(__file__), "template"),
    cookie_secret='neAFBQJ/SsKgIAdExWDXiqJ9s4GwaULHpYsGRbxE0k0=',
    xsrf_cookies = True,
    debug=True
)

mysql_options = dict(
    host="127.0.0.1",
    user="root",
    password="mysql",
    database="ihome"
)

redis_options = dict(
    host="127.0.0.1",
    port=6379
)

log_file = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "warning"


passwd_hash_key = 'SJSHUdeyTg+yEwjtHNLCGIUv2qQlZEbSnzo4yY1sPjg='