import os

basedir = os.path.abspath(os.path.dirname(__file__))


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


class Config(object):
    DEBUG = True
    SECRET_KEY = get_env_variable('SECRET_KEY')
    SESSION_TYPE = 'redis'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user=get_env_variable("POSTGRES_USER"),
                                                                                    pw=os.getenv("POSTGRES_PASSWORD"),
                                                                                    host=os.getenv("POSTGRES_HOST"),
                                                                                    port=os.getenv("POSTGRES_PORT"),
                                                                                    db=os.getenv("POSTGRES_DATABASE"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# class Config(object):
#     MAIL_SERVER = os.environ.get('MAILTRAP_SERVER')
#     MAIL_PORT = 2525
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ.get("MAILTRAP_USERNAM")
#     MAIL_PASSWORD = os.environ.get("MAILTRAP_PASSWORD")

#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     # access to .env and get the value of SECRET_KEY, the variable name can be any but needs to match
#     JWT_SECRET_KEY =  os.environ.get("SECRET_KEY")
    
#     @property
#     def SQLALCHEMY_DATABASE_URI(self):
#         # access to .env and get the value of DATABASE_URL, the variable name can be any but needs to match
#         value = os.environ.get("DATABASE_URL")
#         if not value:
#             raise ValueError("DATABASE_URL is not set")
#         return value

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