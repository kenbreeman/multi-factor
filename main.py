import os

from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

from google.appengine.api import users

import jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

@app.route('/')
def default():
    """Render the main page."""
    template_values = {
        'username': users.get_current_user(),
        'login_url': users.create_login_url('/'),
        'logout_url': users.create_logout_url('/')
    }
    template = JINJA_ENVIRONMENT.get_template('main.html')
    return template.render(template_values)


@app.route('/tokens')
def tokens():
    """Render the token list page"""
    template_values = {
        'username': users.get_current_user(),
        'login_url': users.create_login_url('/'),
        'logout_url': users.create_logout_url('/')
    }
    template = JINJA_ENVIRONMENT.get_template('tokens.html')
    return template.render(template_values)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
