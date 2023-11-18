from enum import Enum

database_info = {
    'dialect': 'mysql',
    'driver': 'pymysql',
    'username': 'chatroom',
    'password': 'chatroom',
    'host': '192.168.6.226',
    'port': '3306',
    'database': 'chatroom'
}

class Config:
    DEBUG = False
    Testing = False
    SQLConnectionURLTemplate = "{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "hyl666"
    SQLALCHEMY_DATABASE_URI = Config.SQLConnectionURLTemplate.format_map(
        database_info
    )
    # 开发环境配置


class TestingConfig(Config):
    TESTING = True
    # 测试环境配置


class ProductionConfig(Config):
    # 生产环境配置
    pass


class ConfigType(Enum):
    DevelopmentConfig = "DevelopmentConfig"
    TestingConfig = "TestingConfig"
    ProductionConfig = "ProductionConfig"


def get_config(config_class: ConfigType):
    res = globals().get(config_class.value)
    if res is None:
        raise ValueError(f"Config class {config_class} not found")
    return res
