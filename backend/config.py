from os import getenv


class BaseConfig:
    RESTPLUS_MASK_SWAGGER = False
    ERROR_404_HELP = False
    MONGO_URI = getenv('MONGO_URI', 'mongodb://localhost:27017/investment-advisor')
    MONGO_USERNAME = getenv('MONGO_USERNAME')
    MONGO_PASSWORD = getenv('MONGO_PASSWORD')


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True


class ProductConfig(BaseConfig):
    pass


config = {
    'dev': DevelopmentConfig,
    'test': TestConfig,
    'prod': ProductConfig
}
