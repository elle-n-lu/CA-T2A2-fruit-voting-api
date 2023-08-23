import os


class Config(object):
    MAIL_SERVER = os.environ.get('MAILTRAP_SERVER')
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAILTRAP_USERNAM")
    MAIL_PASSWORD = os.environ.get("MAILTRAP_PASSWORD")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # access to .env and get the value of SECRET_KEY, the variable name can be any but needs to match
    JWT_SECRET_KEY =  os.environ.get("SECRET_KEY")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # access to .env and get the value of DATABASE_URL, the variable name can be any but needs to match
        value = os.environ.get("DATABASE_URL").replace('postgres://', 'postgresql://')
        if not value:
            raise ValueError("DATABASE_URL is not set")
        return value

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
    
environment = os.environ.get("FLASK_ENV")
if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()