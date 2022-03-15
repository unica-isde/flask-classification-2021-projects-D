from wtforms import FloatField
from wtforms.validators import NumberRange, Optional
from .classification_form import ClassificationForm
from config import Configuration

conf = Configuration()


class ClassificationColorJitterForm(ClassificationForm):
    brightness = FloatField('brightness', render_kw={"placeholder": "0"}, validators=[Optional(), NumberRange(min=0, max=100, message='Must enter a number between 0 and 100')])
    saturation = FloatField('saturation', render_kw={"placeholder": "0"}, validators=[Optional(), NumberRange(min=0, max=100, message='Must enter a number between 0 and 100')])
    contrast = FloatField('contrast', render_kw={"placeholder": "0"}, validators=[Optional(), NumberRange(min=0, max=100, message='Must enter a number between 0 and 100')])
    hue = FloatField('hue', render_kw={"placeholder": "0"}, validators=[Optional(), NumberRange(min=-0.5, max=0.5, message='Must enter a number between -0.5 and 0.5')])

