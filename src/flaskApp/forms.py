from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length


class UserNameForm(FlaskForm):
    user = StringField("Username...", render_kw={"Placeholder" : "Enter summoner name..."}, validators=[Length(min=2)])
    submit = SubmitField()
    example = SubmitField()
    
