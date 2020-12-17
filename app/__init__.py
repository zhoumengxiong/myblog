from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from flask_migrate import Migrate
import click
import os
from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()
migrate = Migrate()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    register_commands(app)
    register_shell_template_context(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


from .models import ArticleType, article_types, Source, Comment, Article, User, Menu, ArticleTypeSetting, BlogInfo, \
    Plugin, BlogView


def register_shell_template_context(app):
    @app.context_processor
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, ArticleType=ArticleType, Source=Source,
                    Comment=Comment, Article=Article, User=User, Menu=Menu,
                    ArticleTypeSetting=ArticleTypeSetting, BlogInfo=BlogInfo,
                    Plugin=Plugin, BlogView=BlogView)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def initblog():
        # step_1:insert basic blog info
        BlogInfo.insert_blog_info()
        # step_2:insert admin account
        User.insert_admin(email='heypython@example.com', username='heypython', password='heypython777')
        # step_3:insert system default setting
        ArticleTypeSetting.insert_system_setting()
        # step_4:insert default article sources
        Source.insert_sources()
        # step_5:insert default articleType
        ArticleType.insert_system_articleType()
        # step_6:insert system plugin
        Plugin.insert_system_plugin()
        # step_7:insert blog view
        BlogView.insert_view()

    @app.cli.command()
    def forge():
        # step_1:insert navs
        Menu.insert_menus()
        # step_2:insert articleTypes
        ArticleType.insert_articleTypes()
        # step_3:generate random articles
        Article.generate_fake(100)
        # step_4:generate random comments
        Comment.generate_fake(300)
        # step_5:generate random replies
        Comment.generate_fake_replies(100)
