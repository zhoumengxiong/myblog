import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))
# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Config(object):
    # DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev key')
    WTF_CSRF_SECRET_KEY = 'random key for form'  # for csrf protection
    JSONIFY_PRETTYPRINT_REGULAR = False

    # Take good care of 'SECRET_KEY' and 'WTF_CSRF_SECRET_KEY', if you use the
    # bootstrap extension to create a form, it is Ok to use 'SECRET_KEY',
    # but when you use tha style like '{{ form.name.labey }}:{{ form.name() }}',
    # you must do this for yourself to use the wtf, more about this, you can
    # take a reference to the book <<Flask Framework Cookbook>>.
    # But the book only have the version of English.
    # @staticmethod
    # def init_app(app):
    #     pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
