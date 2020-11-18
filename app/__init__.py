from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
#mini app for movies
#mini app for auth

def create_app(config):
    #initialization flask app
    app = Flask(__name__)

    # #setup app config
    app.config["SECRET_KEY"] = "21d0a936b67095516de393f969ad2f82"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Secret_123@localhost/iti_movie_app"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    # app.config.from_object(config)
    #Setup extensions
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    from app.modules.movies.views import movie_blueprint, artist_blueprint
    from app.modules.auth.views import auth_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(movie_blueprint)
    app.register_blueprint(artist_blueprint)

    return app
