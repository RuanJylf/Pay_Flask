# -*- coding:utf8 -*-

import logging

# 定义配置类
class Config(object):
    """工程配置信息"""

    DEBUG = True

    # 默认日志等级
    LOG_LEVEL = logging.DEBUG

    # 关闭CSRF保护
    WTF_CSRF_ENABLED = False

    # 密钥
    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"

    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/pugongying"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """开发环境下的配置"""

    DEBUG = True


class ProductionConfig(Config):
    """生产环境下的配置"""

    LOG_LEVEL = logging.WARNING


class TestingConfig(Config):
    """单元测试环境下的配置"""

    DEBUG = True
    TESTING = True


# 定义配置字典
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}


