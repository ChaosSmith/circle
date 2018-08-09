from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

class NewGameForm(Form):
    name = StringField('Game Name', validators=[DataRequired()])
    height = IntegerField('Game Board Height', validators=[DataRequired(),NumberRange(min=10, max=100)])
    length = IntegerField('Game Board Length', validators=[DataRequired(),NumberRange(min=10, max=100)])
    villages = IntegerField('Starting Villages', validators=[DataRequired(),NumberRange(min=1, max=10)])
    password = PasswordField('Optional Password', validators=[])
    submit = SubmitField('Submit')

class JoinGameForm(Form):
    game_id = IntegerField('Game ID', validators=[DataRequired(), NumberRange(min=1)])
    password = PasswordField('Game Password')
    submit = SubmitField('Join')

class CharacterCreationForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    strength = IntegerField('Strength', validators=[DataRequired(),NumberRange(min=6,max=20)])
    dexterity = IntegerField('Dexterity', validators=[DataRequired(),NumberRange(min=6,max=20)])
    constitution = IntegerField('Constitution', validators=[DataRequired(),NumberRange(min=6,max=20)])
    intelligence = IntegerField('Intelligence', validators=[DataRequired(),NumberRange(min=6,max=20)])
    wisdom = IntegerField('Wisdom', validators=[DataRequired(),NumberRange(min=6,max=20)])
    charisma = IntegerField('Charisma', validators=[DataRequired(),NumberRange(min=6,max=20)])
    submit = SubmitField('Create Character')
