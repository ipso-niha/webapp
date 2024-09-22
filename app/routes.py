from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
#importiere von urlib urlparse (werkzeug wird in dieser Version nicht mehr unterstützt)
from urllib.parse import urlparse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResultsForm
from app.models import User, Post, Results

from config import Config

#Route zu Index-Page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
   form = PostForm()
   if form.validate_on_submit():
      post = Post(body=form.post.data, author=current_user)
      db.session.add(post)
      db.session.commit()
      flash('Dein Beitrag ist jetzt online!')
      return redirect(url_for('index'))

   page = request.args.get('page', 1, type=int)
   posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=Config.POSTS_PER_PAGE, error_out=False)

   return render_template('index.html', title='Home Page', form=form, posts=posts.items)

@app.route('/create_result', methods=['GET', 'POST'])
@login_required
def create_result():
   #formP = PostForm()
   formR = ResultsForm()

   #if formP.validate_on_submit():
   #   post = Post(body=formPost.post.data, author=current_user)

   if formR.validate_on_submit():
      result = Results(text=formR.text.data, p1_teamA=formR.p1_teamA.data, p2_teamA=formR.p2_teamA.data, 
                        p1_teamB=formR.p1_teamB.data, p2_teamB=formR.p2_teamB.data,
                        points_teamA=formR.points_teamA.data, points_teamB=formR.points_teamB.data)

      db.session.add(result)
      db.session.commit()
      flash('Dein Resultat-Beitrag ist jetzt online!')
      return redirect(url_for('create_result'))

   page = request.args.get('page', 1, type=int)
   results = Results.query.order_by(Results.date.desc()).paginate(page=page, per_page=Config.POSTS_PER_PAGE, error_out=False)

   return render_template('create_result.html', title='Resultat erfassen', formR=formR, results=results.items)


@app.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = LoginForm()
   if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user is None or not user.check_password(form.password.data):
         flash('Invalid username or password')
         return redirect(url_for('login'))
      login_user(user, remember=form.remember_me.data)
      next_page = request.args.get('next')
      if not next_page or urlparse(next_page).netloc != '':
         next_page = url_for('index')
      return redirect(next_page)
   return render_template('login.html', title='Sign In', form=form)

#Route für das Registrierungs-Form
@app.route('/register', methods=['GET', 'POST'])
def register():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = RegistrationForm()
   if form.validate_on_submit():
# Route /register wurde mit POST betreten. Prüfen, ob alles ok ist:
      user = User(username=form.username.data, email=form.email.data)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      flash('Congratulations, you are now a registered user!')
      return redirect(url_for('login'))
# Route /register wurde mit GET betreten
   return render_template('register.html', title='Register', form=form)

#Route für die Logout-Funktion
@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('index'))

#Route für Benutzerprofil darstellung
@app.route('/user/<username>')
@login_required
def user(username):
   user = User.query.filter_by(username=username).first_or_404()
   posts = [
      {'author': user, 'body': 'Test post 1'},
      {'author': user, 'body': 'Test post 2'}
   ]
   return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
   if current_user.is_authenticated:
      current_user.last_seen = datetime.utcnow()
      db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
   form = EditProfileForm()
   if form.validate_on_submit():
      current_user.username = form.username.data
      current_user.about_me = form.about_me.data
      current_user.birthday = form.birthday.data
      db.session.commit()
      flash('Änderungen wurden gespeichert.')
      return redirect(url_for('edit_profile'))
   elif request.method == 'GET':
      form.username.data = current_user.username
      form.about_me.data = current_user.about_me
      form.birthday.data = current_user.birthday
   return render_template('edit_profile.html', title='Profil bearbeiten', form=form)


