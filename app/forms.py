from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired()])
   password = PasswordField('Password', validators=[DataRequired()])
   remember_me = BooleanField('Remember Me')
   submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired()])
   email = StringField('Email', validators=[DataRequired(), Email()])
   password = PasswordField('Password', validators=[DataRequired()])
   password2 = PasswordField(
      'Repeat Password', validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('Register')

   def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user is not None:
         raise ValidationError('Bitte verwende einen anderen Benutzernamen.')

   def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user is not None:
         raise ValidationError('Bitte verwende eine andere E-Mail Adresse.')

class EditProfileForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired()])
   about_me = TextAreaField('Über mich', validators=[Length(min=0, max=200)])
   birthday = DateField('Geburtstag')
   submit = SubmitField('Submit')

class PostForm(FlaskForm):
   post = TextAreaField('Dein Beitrag', validators=[DataRequired()])
   submit = SubmitField('Submit')

class ResultsForm(FlaskForm):
    text = TextAreaField('Dein Beitrag', validators=[DataRequired()])
    p1_teamA = TextAreaField('S1 Team A', validators=[DataRequired()])
    p2_teamA = TextAreaField('S2 Team A', validators=[DataRequired()])
    p1_teamB = TextAreaField('S1 Team B', validators=[DataRequired()])
    p2_teamB = TextAreaField('S2 Team B', validators=[DataRequired()])
    points_teamA = IntegerField('Punkte Team A', validators=[DataRequired()])
    points_teamB = IntegerField('Punkte Team B', validators=[DataRequired()])
    submit = SubmitField('Submit')
