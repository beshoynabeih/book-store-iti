import os

class AppConfig():

    SECRET_KEY = os.environ.get("SECRET_KEY") or "21d0a936b67095516de393f969ad2f82"
    # SQLALCHEMY_DATABASE_URI = os.environ.get("APP_DATABASE_URI") or "postgresql://postgres:Secret_123@localhost/iti_movie_app"
    SQLALCHEMY_TRACK_MODIFICATIONS = True