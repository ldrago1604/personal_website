"""
__init__.py is used to create initial app or starting point of flask application
from this file we manage all other python files
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import secrets

# define database in db
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # we create an instance of this class. The first argument is the name of the application’s module or package.
    # __name__ is a convenient shortcut for this that is appropriate for most cases. This is needed so that Flask knows
    # where to look for resources such as templates and static files.
    app = Flask(__name__)
    secret = secrets.token_urlsafe(32)
    app.secret_key = secret
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)  # initialize db

    from .views import views
    from .auth import auth

    # Import and register the blueprint from the factory using app.register_blueprint().
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
