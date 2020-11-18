from flask import Blueprint, request, render_template, redirect, flash, url_for
from app.modules.movies.models import Movie, Genre, Artist
from .forms import MovieForm, ArtistForm
from flask_login import current_user
from app import db
import os
from datetime import datetime

IMAGES_UPLOADS_DIR = "/var/www/html/ITI/Python/flask/Day2/lab2/starter_project/app/static/images/avatars"


movie_blueprint = Blueprint('movies', __name__, template_folder='templates')
artist_blueprint = Blueprint('artists', __name__, template_folder='templates')

@movie_blueprint.route("/", methods=["GET"])
@movie_blueprint.route("/home", methods=["GET"])
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('movies/index.html', movies=movies)


@movie_blueprint.route("/movie/<id>")
def movie(id):
    movie = Movie.query.get_or_404(id)
    return render_template('movies/movie.html', movie=movie)


@movie_blueprint.route("/movie/<id>/edit", methods=["GET", "POST"])
def movie_edit(id):
    if current_user.is_authenticated:
        movie_form = MovieForm()
        movie_form.genres.choices = [(genre.id, genre.name)
                                    for genre in Genre.query.all()]
        if request.method == "POST":
            if movie_form.validate_on_submit():
                movie = Movie.query.get(id)
                movie.title = movie_form.title.data
                movie.description = movie_form.description.data
                movie.releas_year = movie_form.year.data
                movie.genres = Genre.query.filter(
                    Genre.id.in_(movie_form.genres.data)).all()

                db.session.commit()
                flash("Movie updated successfully", "success")
                return redirect(url_for("movies.index"))

            else:
                flash("Something went wrong", "danger")
                movie = Movie.query.get(id)
                selected_genres = [genre.id for genre in movie.genres]
                return render_template("movies/movies.html",
                                    form=movie_form,
                                    movie=movie,
                                    selected_genres=selected_genres)
        else:
            movie = Movie.query.get(id)
            selected_genres = [genre.id for genre in movie.genres]
            return render_template("movies/movies.html",
                                form=movie_form,
                                movie=movie,
                                selected_genres=selected_genres)
    else:
        return render_template("auth/login.html")


@movie_blueprint.route("/movies", methods=["GET", "POST"])
def movies_form():
    if current_user.is_authenticated:
        movie_form = MovieForm()
        movie_form.genres.choices = [(genre.id, genre.name)
                                    for genre in Genre.query.all()]
        movie_form.artists.choices = [(artist.id, artist.first_name + ' ' + artist.last_name) for artist in Artist.query.all() ]
        if request.method == "POST":
            if movie_form.validate_on_submit():
                genres = Genre.query.filter(Genre.id.in_(
                    movie_form.genres.data)).all()
                movie = Movie(title=movie_form.title.data,
                            description=movie_form.description.data,
                            releas_year=movie_form.year.data,
                            genres=genres
                            )
                db.session.add(movie)
                db.session.commit()
                flash("Movie add successfully", "success")
                return redirect(url_for("movies.index"))

            else:
                return render_template("movies/movies.html", form=movie_form)
        else:
            return render_template("movies/movies.html", form=movie_form)
    else:
        # return render_template(url_for("auth.login"))
        return render_template("auth/login.html")

  
@movie_blueprint.route("/movie/<id>/delete", methods=["GET"])
def movie_delete(id):
    Movie.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("movies.index"))

# Artist routes

@artist_blueprint.route('/artists', methods=["GET"])
def artists():
    artists = Artist.query.all()
    return render_template('movies/artists.html', artists=artists)


@artist_blueprint.route("/artist/add", methods=["GET", "POST"])
def artist_form():
    artist_form = ArtistForm()
    if request.method == "POST":
        if artist_form.validate_on_submit():
            # genres = Genre.query.filter(Genre.id.in_(
            #     movie_form.genres.data)).all()
            if request.files:
                avatar = request.files['avatar']
                # print(request.files.get("avatar").content_type)
                avatar_name = ''
                if avatar:
                    avatar_name = str(datetime.now()) + avatar.filename
                    avatar.save(os.path.join(IMAGES_UPLOADS_DIR, avatar_name))   
            artist = Artist(first_name=artist_form.first_name.data,
                            last_name=artist_form.last_name.data,
                            birth_date=artist_form.birth_date.data,
                            nationality=artist_form.nationality.data,
                            avatar=avatar_name
                          )
            db.session.add(artist)
            db.session.commit()

            flash("artist added successfully", "success")
            return redirect(url_for("artists.artists"))

        else:
            return render_template("movies/add_artist.html", form=artist_form)
    else:
        return render_template("movies/add_artist.html", form=artist_form)


@artist_blueprint.route("/artist/<id>", methods=["GET", "POST"])
def artist(id):
    artist = Artist.query.get_or_404(id)
    return render_template('movies/artist.html', artist=artist)


@artist_blueprint.route("/artist/<id>/edit", methods=["GET", "POST"])
def artist_edit(id):
    artist_form = ArtistForm()
    if request.method == "POST":
        if artist_form.validate_on_submit():
            artist = Artist.query.get(id)
            artist.first_name = artist_form.first_name.data
            artist.last_name = artist_form.last_name.data
            artist.birth_date = artist_form.birth_date.data
            artist.nationality = artist_form.nationality.data
            if request.files:
                avatar = request.files['avatar']
                avatar_name = str(datetime.now()) + avatar.filename
                avatar.save(os.path.join(IMAGES_UPLOADS_DIR, avatar_name))
                artist.avatar = avatar_name
            db.session.commit()
            flash("artist updated successfully", "success")
            return redirect(url_for("artists.artists"))

        else:
            flash("Something went wrong", "danger")
            artist = Artist.query.get(id)
            return render_template("movies/add_artist.html",
                                   form=artist_form,
                                   artist=artist)
    else:
        artist = Artist.query.get(id)
        return render_template("movies/add_artist.html",
                               form=artist_form,
                               artist=artist)


@artist_blueprint.route("/artist/<id>/delete", methods=["GET"])
def artist_delete(id):
    # delete Pivot table
    Artist.query.filter_by(id=id).delete()
    db.session.commit()
    flash("artist deleted successfully", "info")
    return redirect(url_for("artists.artists"))
