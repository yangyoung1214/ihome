# @Time    : 2019/6/8 22:23
# @Author  : young
import redis


class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@127.0.0.1:3306/my-ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400

    # wtf
    SECRET_KEY = "hard to guess"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config = {
    "develop": DevelopmentConfig,
    "Product": ProductionConfig
}
