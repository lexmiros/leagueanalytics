
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class UserNameForm(FlaskForm):
    user = StringField("Username...", render_kw={"Placeholder" : "Summoner name..."})
    region = SelectField("Region", choices=[('OC1', 'OCE'), ('NA1', 'NA'), ('BR', 'BR'), ('EUN1', 'EUN'), ('EUW1', 'EUW')
        , ('JP1', 'JP'), ('KR', 'KR'), ('LA1', 'LA1'), ('LA2', 'LA2'), ('TR1', 'TR'), ('RU', 'RU')],
        validators=[DataRequired()])
    submit = SubmitField()
    example = SubmitField()

class LoadForm(FlaskForm):
    Load = SubmitField()
    
