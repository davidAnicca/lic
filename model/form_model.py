from wtforms import Form, FloatField, IntegerField, StringField, validators
from math import pi

class InputForm(Form):
    G = IntegerField(
        label='Number of generations', default=50,
        validators=[validators.InputRequired()])
    P = IntegerField(
        label='Population size', default=1000,
        validators=[validators.InputRequired()])
    M = FloatField(
        label='Mutation rate', default=0.2,
        validators=[validators.InputRequired()])
    A = StringField(
        label="Input amino-acid chain", default="PHHHHP",
        validators=[validators.InputRequired()]
    )