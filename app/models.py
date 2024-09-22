from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(64), index=True, unique=True)
   email = db.Column(db.String(120), index=True, unique=True)
   password_hash = db.Column(db.String(256))
   posts = db.relationship('Post', backref='author', lazy='dynamic')
   about_me = db.Column(db.String(200))
   last_seen = db.Column(db.DateTime, default=datetime.utcnow)
   birthday = db.Column(db.Date)

   def __repr__(self):
      return '<User {}>'.format(self.username)

   def set_password(self, password):
      self.password_hash = generate_password_hash(password)

   def check_password(self, password):
      return check_password_hash(self.password_hash, password)

   def all_posts(self):
      own = Post.query.filter_by(user_id=self.id)

@login.user_loader
def load_user(id):
   return User.query.get(int(id))

class Post(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   body = db.Column(db.String(140))
   timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

   def __repr__(self):
      return '<Post {}>'.format(self.body)

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    p1_teamA = db.Column(db.String(30))
    p2_teamA = db.Column(db.String(30))
    p1_teamB = db.Column(db.String(30))
    p2_teamB = db.Column(db.String(30))
    points_teamA = db.Column(db.Integer)
    points_teamB = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
       return '<Results {}>'.format(self.text)
