import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    FLASK_ENV=os.getenv('FLASK_ENV')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY=os.getenv('SECRET_KEY')
    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=os.getenv('MAIL_PORT')
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS')
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL')
    WT_BLACKLIST_ENABLED =  os.getenv('WT_BLACKLIST_ENABLED')
    JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS')



class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
