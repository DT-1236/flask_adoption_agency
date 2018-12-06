from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import URL, Optional, InputRequired, NumberRange, ValidationError


class LocalOrURL(URL):
    def __call__(self, form, field):
        if (' ' in field.data) and (field.data.split(' ')[1:] == [
                'on', 'file'
        ]):
            # Consider making a hidden field before rendering which matches the extension on record
            # photo_utl for locally storied images actually like ".ext on file"
            return

        # If field input does not indicate locally stored image, run original URL validator call
        message = self.message
        if message is None:
            message = field.gettext('Invalid URL.')

        match = super(URL, self).__call__(form, field, message)
        if not self.validate_hostname(match.group('host')):
            raise ValidationError(message)


def xor_photo_validate(self):
    """Exclusive OR validation for the image upload and the photo_url inputs
    This validation only allows one"""

    if not FlaskForm.validate(self):
        return False

    # The XOR validation only happens after the original validations on the form have been run
    if self.photo_url.data and self.uploaded_photo.data:
        self.photo_url.errors.append("Only one photo is allowed")
        self.uploaded_photo.errors.append("Only one photo is allowed")
        return False
    return True


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
    photo_url = StringField(
        "Picture URL", validators=[Optional(), LocalOrURL()])
    uploaded_photo = FileField(
        "Upload a photo",
        validators=[
            Optional(),
            FileAllowed(['png', 'jpg', 'tif', 'tiff', 'gif'])
        ])
    notes = TextAreaField("Notes")

    def validate(self):
        return xor_photo_validate(self)


class EditPetForm(FlaskForm):
    """Update fancy pets"""

    notes = TextAreaField("Notes")
    available = BooleanField("Available")
    photo_url = StringField(
        "Picture URL", validators=[Optional(), LocalOrURL()])
    uploaded_photo = FileField(
        "Upload a photo",
        validators=[
            Optional(),
            FileAllowed(['png', 'jpg', 'tif', 'tiff', 'gif'])
        ])

    def validate(self):
        return xor_photo_validate(self)
