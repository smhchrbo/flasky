'''程序的配置'''
import  os
basedir = os.path.abspath(os.path.dirname(__file__))

#基类包含通用配置类
class Config:
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess String'
        SQLALCHEMY_COMMIT_ON_TEARDOWN = True
        FLASKY_MAIL_SUBJECT_PREFIX = '[flasky]'
        FLASY_MAIL_SENDER = 'flasky admin <flasky@example.com>'
        FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

        #参数是程序实例
        @staticmethod
        def init_app(app):
            pass

#子类包含其他配置类，开发环境配置
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    SQLALCHEMY_DATABASE_URI =os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

#子类包含其他配置类，测试环境配置
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI =os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

#子类包含其他配置类，生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

#config 字典中注册了不同的配置环境，而且还注册了一个默认配置
config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}