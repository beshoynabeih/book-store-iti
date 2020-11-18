from app import db


Moves_Genres = db.Table(
    'movies_genres',
    db.Column('movie_id',
              db.Integer,
              db.ForeignKey('movies.id'),
              nullable=False),
    db.Column('genre_id',
              db.Integer,
              db.ForeignKey('genres.id'),
              nullable=False))

Movies_Artists = db.Table(
    'movies_artists',
    db.Column('movie_id',
              db.Integer,
              db.ForeignKey('movies.id'),
              nullable=False),
    db.Column('artist_id',
              db.Integer,
              db.ForeignKey('artists.id'),
              nullable=False))

Movies_Likes = db.Table(
    'movies_likes',
    db.Column('movie_id',
                db.Integer,
                db.ForeignKey('movies.id'),
                nullable=False),
    db.Column('user_id',
                db.Integer,
                db.ForeignKey('users.id'),
                nullable=False))


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    releas_year = db.Column(db.Date, nullable=False)
    genres = db.relationship('Genre',
                             secondary=Moves_Genres,
                             backref='movies',
                             cascade='delete',
                             lazy=True)


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(50), nullable=True)

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    nationality = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(100), nullable=True)
    # movies = db.relationship('Movie',
    #                          secondary=Movies_Artists,
    #                          backref='artists',
    #                          cascade='delete',
    #                          lazy=True)
    def __repr__(self):
        return self.first_name