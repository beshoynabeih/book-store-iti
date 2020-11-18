from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateField

GENRES = ["Action", "Romance", "Drama", "Horror", "Historical", "Documentary"]


class MovieForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(),
                                    Length(min=1, max=25)])
    description = TextAreaField(
        "Description", validators=[DataRequired(),
                                   Length(min=1, max=500)])
    year = DateField("Release Date",
                     validators=[DataRequired()],
                     format="%Y-%m-%d")
    genres = SelectMultipleField("Genres", coerce=int)
    submit = SubmitField('Add')
