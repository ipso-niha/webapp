from app import app
from app.models import User, Results #, Post

@app.shell_context_processor
def make_shell_context():
   return {'db': db, 'User': User, 'Results': Results}

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
