import os

'''
相关配置参数
'''
class BaseConfig:

    '''
    通用配置
    '''


    DEBUG       = True # 允许调试，在正式平台上需要关闭
    SECRET_KEY  = 'this is a secret key!'   # session
    WEB_USER = 'admin'
    WEB_PASS = 'honghusec'
    WEB_HOST = '0.0.0.0'  # Web Server Host
    WEB_PORT = 5000  # Web Server Port


Config = {
    'base': BaseConfig
}