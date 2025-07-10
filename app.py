import os
from flask import Flask, render_template
from flask_login import LoginManager, current_user, AnonymousUserMixin
from modules import register_modules
from config import Config

# Zet omgevingsvariabelen
os.environ.setdefault('FLASK_APP', 'app.py')
os.environ.setdefault('FLASK_ENV', 'development')

# Maak de Flask-app aan
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)
app.config.from_object(Config)

# Init login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Dummy user loader: we hebben geen echte users,
# dus geven we altijd None terug. current_user wordt dan AnonymousUserMixin.
@login_manager.user_loader
def load_user(user_id):
    return None

# Zorg dat current_user altijd beschikbaar is in Jinja
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Registreer al je submodules (o.a. /thumbnail)
register_modules(app)

# Landing page
@app.route('/')
def landing():
    return render_template('landing.html')

if __name__ == "__main__":
    app.run(debug=True)
