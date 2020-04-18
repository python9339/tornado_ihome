# -*- coding: utf-8 -*-
# @Time    : 20-4-13 下午3:45
# @File    : urls.py
import os

from handlers import passport,verifycode,myihome
from handlers.basehandler import StaticFileHandler

handlers = [
    (r'/api/register',passport.RegisterHandler),
    (r'/api/login',passport.LoginHandler),
    (r'/api/checkLogin', passport.CheckLoginHandler),
    (r'/api/getImageCode', verifycode.PicCodeHandler),
    (r'/api/smsCode', verifycode.SmsCodeHandler),
    (r'/api/myihome', myihome.MyIhomeHandler),
    (r'/(.*)', StaticFileHandler, {'path':os.path.join(os.path.dirname(__file__), "html"), 'default_filename':'index.html'})
]