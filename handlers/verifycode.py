# -*- coding: utf-8 -*-
# @Time    : 20-4-14 上午10:03
# @File    : verifycode.py
import logging
import constants
import re
import random
from basehandler import BaseHandler
from utils.captcha import captcha
from utils.response_code import RET
from libs.yuntongxun.SendTemplateSMS import ccp


class PicCodeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        # 获取前段传过来的codeid
        code_id = self.get_argument('codeid')
        # 根据code_id生成验证码
        name, text, pic = captcha.captcha.generate_captcha()
        # 从浏览器中获取保存在cookie中的code_id,如果没有，返回None
        cookie_code_id = self.get_secure_cookie("pre_code_id")
        # # 判断cookie_code_id是否存在，如果存在，则在redis中删除掉
        try:
            if cookie_code_id:
                # 如果cookie_code_id存在，则在redis中删除掉
                self.redis.delete("pic_code_%s" % cookie_code_id)
        except Exception as e:
            logging.error(e)
            self.write("")
        # 将codeid对应的text存在redis中
        self.redis.setex("pic_code_%s" % code_id, constants.PIC_CODE_EXPIRES_SECONDS , text)

        # 将当前的codeid设置在cookie中，以便更新验证码时将其从redis中删除掉
        self.set_secure_cookie("pre_code_id", code_id)

        # 返回图片验证码
        self.set_header('Content-Type', 'image/jpg')
        self.write(pic)

# 短信验证码处理类
class SmsCodeHandler(BaseHandler):
    """
    errorcode,errormsg来向前段传递信息
    RET.OK       =  0
    RET.NODATA   =  4002
    RET.DATAERR  =  4004
    RET.THIRDERR =  4301
    """
    def post(self, *args, **kwargs):
        # 接收前段传过来的json数据(mobile, image_code_text, image_code_id)
        mobile = self.json_args.get('mobile')
        image_code_text = self.json_args.get('image_code_text')
        image_code_id = self.json_args.get('image_code_id')

        # print mobile, image_code_id, image_code_text
        # 判断这三个数据是否都存在，如果有其中一个数据为空，则返回相关json数据{error_num:RET.NODATA, error_msg:'不能为空'}
        if not all((mobile, image_code_text, image_code_id)):
            return self.write(dict(errorcode=RET.NODATA, errormsg='不能为空'))

        # 判断用户输入的手机号码是否符合以１开头的11位号码，不符合返回json数据{error_num:RET.DATAERR, error_msg:'请输入11位数的手机号码'}
        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errorcode=RET.NODATA, errormsg='请输入11位数的手机号码'))

        # 获取图片验证码真实值
        try:
            real_image_code_text = self.redis.get("pic_code_%s" % image_code_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errorcode=RET.DBERR, errormsg='查询验证码错误'))

        print real_image_code_text
        # 如果数据为空，则说明验证码过期
        if not real_image_code_text:
            return self.write(dict(errorcode=RET.NODATA, errormsg='验证码过期'))

        # 删除保存在Redis中的图片验证码
        try:
            self.redis.delete("pic_code_%s" % image_code_id)
        except Exception as e:
            logging.error(e)

        # 判断用户传递过来的图片验证码文本是否和存在Redis数据库中的相同，不相同返回json数据{error_num:RET.DATAERR, error_msg:'验证码输入错误'}
        if image_code_text.lower() != real_image_code_text.lower():
            return self.write(dict(errorcode=RET.DATAERR, errormsg='验证码输入错误'))

        # 随机生成四位验证码并保存在Redis数据库中，如保存不成功，返回json数据{error_num:RET.DBERR, error_msg:'验证码存入数据库出错'}
        sms_code = "%04d" % random.randint(1, 9999)
        try:
            self.redis.setex('sms_code_%s' % mobile, constants.SMS_CODE_EXPIRES_SECONDS, sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errorcode=RET.DBERR, errormsg='验证码存入数据库出错'))

        # 向mobile发送随机生成的验证码，发送不成功，返回json数据{error_num:RET.THIRDERR, error_msg:'第三方系统错误'}
        try:
            result = ccp.sendTemplateSMS(mobile, [sms_code, constants.SMS_CODE_EXPIRES_SECONDS/60], 1)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errorcode=RET.THIRDERR, errormsg='发送短信失败'))

        if result:
            # 成功返回json数据{error_num:RET.OK, error_msg:'成功发送短信验证码'}
            self.write(dict(errorcode=RET.OK, errormsg='成功发送短信验证码'))
        else:
            self.write(dict(errorcode=RET.UNKOWNERR, errormsg='发送短信失败'))