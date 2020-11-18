from flask import Blueprint, request, render_template, redirect, flash, url_for
from app.modules.movies.models import Movie, Genre
from .forms import MovieForm
from flask_login import current_user
from app import db

movie_blueprint = Blueprint('movies', __name__, template_folder='templates')

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


@movie_blueprint.route("/movies", methods=["GET", "POST"])
def movies_form():
    if current_user.is_authenticated:
        movie_form = MovieForm()
        movie_form.genres.choices = [(genre.id, genre.name)
                                    for genre in Genre.query.all()]
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
