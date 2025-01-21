from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadLeafForm(FlaskForm):
    image = FileField('Upload an Image of the Leaf', validators=[DataRequired()])
    submit = SubmitField('Upload')
