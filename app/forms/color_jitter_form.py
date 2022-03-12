from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import NumberRange, DataRequired

from app.utils.list_images import list_images
from config import Configuration

conf = Configuration()


class ClassificationColorJitterForm(FlaskForm):
    brightness = FloatField('brightness', validators=[NumberRange(min=0, message='Must enter a number greater or equal than 0')])
    saturation = FloatField('saturation', validators=[NumberRange(min=0, message='Must enter a number greater or equal than 0')])
    contrast = FloatField('contrast', validators=[NumberRange(min=0, message='Must enter a number greater or equal than 0')])
    hue = FloatField('hue', validators=[NumberRange(min=-0.5, max=0.5, message='Must enter a number between -0.5 and 0.5')])

    model = SelectField('model', choices=conf.models, validators=[DataRequired()])
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    submit = SubmitField('Submit')
