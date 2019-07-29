from os import getenv


class BaseConfig:
    RESTPLUS_MASK_SWAGGER = False


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
