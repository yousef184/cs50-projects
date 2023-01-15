from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


class UpdateAccountForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])