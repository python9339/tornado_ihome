# -*- coding: utf-8 -*-
# @Time    : 20-4-13 下午4:40
# @File    : handlers.py
import logging
import re
import hashlib
import config
from utils.response_code import RET
from utils.session import Session
from basehandler import BaseHandler


class RegisterHandler(BaseHandler):

    def post(self, *args, **kwargs):
        # 获取前端传递过来的JSON数据，并将其提取出来
        mobile = self.json_args.get('mobile')
        smsCode = self.json_args.get('phoneCode')
        password = self.json_args.get('password')
        password2 = self.json_args.get('password2')

        # 判断传递过来的参数是否为空
        if not all((mobile, smsCode, password, password2)):
            return self.write(dict(errorcode=RET.NODATA, errormsg='参数不完整'))

        # 判断手机号输入格式是否正确
        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errorcode=RET.NODATA, errormsg='输入手机号码不正确'))

        # 判断两次输入的密码是否相同
        if password != password2:
            return self.write(dict(errorcode=RET.PARAMERR, errormsg='两次输入密码不一致'))

        # # 判断手机验证码是否正确
        # try:
        #     real_sms_code = self.redis.get('sms_code_%s' % mobile)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errorcode=RET.DBERR, errormsg='查询短信验证码出错'))
        # # 判断短信验证码是否过期
        # if not real_sms_code:
        #     return self.write(dict(errorcode=RET.DBERR, errormsg='短信验证码过期'))
        # # 对比用户填写的验证码与真实值
        # if smsCode != real_sms_code:
        #     return self.write(dict(errorcode=RET.DATAERR, errormsg='短信验证码输入有误'))
        # # 删除掉存储在Redis中的短信验证码
        # try:
        #     self.redis.delete('sms_code_%s' % mobile)
        # except Exception as e:
        #     logging.error(e)

        # 保存数据，同时判断手机号是否存在，判断的依据是数据库中mobile字段的唯一约束
        password = hashlib.sha256(password + config.passwd_hash_key).hexdigest()
        sql_str = "insert into ih_user_profile(up_name, up_mobile, up_passwd) values (%(name)s, %(mobile)s, %(passwd)s);"
        try:
            user_id = self.db.execute(sql_str, name=mobile, mobile=mobile, passwd=password)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errorcode=RET.DBERR, errormsg='手机号码已被注册'))

        # 用session记录用户的登录状态
        session = Session(self)
        session.data['user_id'] = user_id
        session.data['mobile'] = mobile
        session.data['name'] = mobile
        try:
            session.save()
        except Exception as e:
            logging.error(e)

        return self.write(dict(errorcode=RET.OK, errormsg='注册成功'))


class LoginHandler(BaseHandler):

    def post(self, *args, **kwargs):
        # 获取前端传递过来的JSON数据，并将其提取出来
        mobile = self.json_args.get('mobile')
        password = self.json_args.get('password')

        # 检查参数
        if not all([mobile, password]):
            return self.write(dict(errorcode=RET.PARAMERR, errormsg="参数错误"))
        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errorcode=RET.DATAERR, errormsg="手机号错误"))

        # 检查秘密是否正确
        res = self.db.get("select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s",
                          mobile=mobile)
        password = hashlib.sha256(password + config.passwd_hash_key).hexdigest()

        if res and res["up_passwd"] == unicode(password):
            # 生成session数据
            # 返回客户端
            try:
                self.session = Session(self)
                self.session.data['user_id'] = res['up_user_id']
                self.session.data['name'] = res['up_name']
                self.session.data['mobile'] = mobile
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write(dict(errorcode=RET.OK, errormsg="OK"))
        else:
            return self.write(dict(errorcode=RET.DATAERR, errormsg="手机号或密码错误！"))

class CheckLoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        #　如果返回真，则说明data中有数据
        if self.get_current_user():
            return self.write(dict(errorcode=RET.OK, errormsg="true", data={"name":self.session.data['name']}))
        else:
            return self.write(dict(errorcode=RET.USERERR, errormsg="false"))
