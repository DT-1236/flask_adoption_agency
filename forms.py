from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import URL, Optional, InputRequired, NumberRange


class AddPetForm(FlaskForm):
    """Fancy form for fancy pets"""

    name = StringField("Name", validators=[InputRequired()])
    species = SelectField(
        "Species",
        validators=[InputRequired()],
        choices=[('dog', 'Dog'), ('cat', 'Cat'), ('porcupine', 'Porcupine')])
    age = IntegerField(
        "Age",
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=30,
                message="Age must be between %(min)s and %(max)s")
        ])
    photo_url = StringField("Picture URL", validators=[Optional(), URL()])
    notes = TextAreaField("Notes")


class EditPetForm(FlaskForm):
    """Update fancy pets"""

    photo_url = StringField("Picture URL", validators=[Optional(), URL()])
    notes = TextAreaField("Notes")
    available = BooleanField("Available")
