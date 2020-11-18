from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateField


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
    artists = SelectMultipleField("Artists", coerce=int)
    submit = SubmitField('Add')

class ArtistForm(FlaskForm):
    first_name = StringField('First Name',
                        validators=[DataRequired(),
                                    Length(min=1, max=25)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(),
                            Length(min=1, max=25)])
    birth_date = DateField('Birth Date',
                           validators=[DataRequired()],
                           format="%Y-%m-%d")
    nationality = StringField('Nationality',
                              validators=[DataRequired(),
                               Length(min=1, max=25)])
    avatar = FileField('Profile Picture')
    submit = SubmitField('Add')