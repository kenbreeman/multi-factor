import os

from flask import Flask
from flask import redirect

app = Flask(__name__)
app.config['DEBUG'] = True

from google.appengine.api import users
from api import get_mfa_user

import jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def is_valid_user():
    appengine_user = users.get_current_user()
    if not appengine_user:
        return False
    mfa_user = get_mfa_user(appengine_user)
    if not mfa_user:
        return False
    return True


@app.route('/')
def default():
    """Render the main page."""
    template_values = {
        'username': users.get_current_user(),
        'validuser': is_valid_user(),
        'login_url': users.create_login_url('/'),
        'logout_url': users.create_logout_url('/')
    }
    template = JINJA_ENVIRONMENT.get_template('main.html')
    return template.render(template_values)


@app.route('/signup')
def signup():
    """Render the signup page."""
    validuser = is_valid_user()
    if validuser:
        return redirect('/tokens', code=307)

    template_values = {
        'username': users.get_current_user(),
        'validuser': validuser,
        'login_url': users.create_login_url('/'),
        'logout_url': users.create_logout_url('/')
    }
    template = JINJA_ENVIRONMENT.get_template('signup.html')
    return template.render(template_values)


@app.route('/tokens')
def tokens():
    """Render the token list page"""
    validuser = is_valid_user()
    if not validuser:
        return redirect('/signup', code=307)

    template_values = {
        'username': users.get_current_user(),
        'validuser': validuser,
        'login_url': users.create_login_url('/'),
        'logout_url': users.create_logout_url('/')
    }
    template = JINJA_ENVIRONMENT.get_template('tokens.html')
    return template.render(template_values)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return '', 404
