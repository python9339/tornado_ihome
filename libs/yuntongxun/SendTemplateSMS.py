#-*- coding: UTF-8 -*-
from CCPRestSDK import REST
import ConfigParser
import logging

accountSid = '8aaf07087172a6ee0171780aa8b2036b';
# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。

accountToken = 'a90ddf2c2c4a410c8011d1c0b1ed1878';
# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。

appId = '8aaf07087172a6ee0171780aa91d0372';
# 请使用管理控制台中已创建应用的APPID。

serverIP = 'app.cloopen.com';
# 说明：请求地址，生产环境配置成app.cloopen.com。

serverPort = '8883';
# 说明：请求端口 ，生产环境为8883.

softVersion = '2013-12-26';  # 说明：REST API版本号保持不变。

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

# def sendTemplateSMS(to,datas,tempId):
#
#
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)


class CCP(object):

    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @staticmethod
    def instance():
        if not hasattr(CCP, "_instance"):
            CCP._instance = CCP()
        return CCP._instance

    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result = self.rest.sendTemplateSMS(to, datas, tempId)
        except Exception as e:
            logging.error(e)
            raise e

        # print result
        # for k, v in result.iteritems():
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        if result.get("statusCode") == "000000":
            return True
        else:
            return False

ccp = CCP.instance()

if __name__ == "__main__":
    ccp = CCP.instance()
    ccp.sendTemplateSMS("17689839339", ["4567", 10], 1)



   
#sendTemplateSMS(手机号码,内容数据,模板Id)