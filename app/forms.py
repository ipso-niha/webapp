from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
   username = StringField('Benutzername', validators=[DataRequired()])
   password = PasswordField('Passwort', validators=[DataRequired()])
   remember_me = BooleanField('Angemeldet bleiben')
   submit = SubmitField('Anmelden')

class RegistrationForm(FlaskForm):
   username = StringField('Benutzername', validators=[DataRequired()])
   email = StringField('E-Mail', validators=[DataRequired(), Email()])
   password = PasswordField('Passwort', validators=[DataRequired()])
   password2 = PasswordField(
      'Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('Registrieren')

   def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user is not None:
         raise ValidationError('Bitte verwende einen anderen Benutzernamen.')

   def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user is not None:
         raise ValidationError('Bitte verwende eine andere E-Mail Adresse.')

class EditProfileForm(FlaskForm):
   username = StringField('Benutzername', validators=[DataRequired()])
   about_me = TextAreaField('Über mich', validators=[Length(min=0, max=200)])
   birthday = DateField('Geburtstag')
   submit = SubmitField('Speichern')

class ResultsForm(FlaskForm):
    text = TextAreaField('Dein Beitrag', validators=[DataRequired()])
    p1_teamA = TextAreaField('Spieler 1 Team A', validators=[DataRequired()])
    p2_teamA = TextAreaField('Spieler 2 Team A', validators=[DataRequired()])
    p1_teamB = TextAreaField('Spieler 1 Team B', validators=[DataRequired()])
    p2_teamB = TextAreaField('Spieler 2 Team B', validators=[DataRequired()])
    points_teamA = IntegerField('Punkte Team A', validators=[DataRequired()])
    points_teamB = IntegerField('Punkte Team B', validators=[DataRequired()])
    submit = SubmitField('Beitrag abschicken')
