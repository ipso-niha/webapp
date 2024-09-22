import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'erraetst-Du-nie'
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
      'sqlite:///' + os.path.join(basedir, 'app.db')
   SQLALCHEMY_TRACK_MODIFICATIONS = False

   POSTS_PER_PAGE = 5
   
   SERVER_NAME = '172.161.147.246:8080'
