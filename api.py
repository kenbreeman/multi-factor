from otp_token import Token
from otp_token import OrderedToken
from mfa_user import User

from google.appengine.ext import db
from google.appengine.api import users

from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
app = Flask(__name__)
app.config['DEBUG'] = True

from pyotp import TOTP
from Crypto.Cipher import AES 
from appengine_config import SECRET_KEY

import cgi


def get_mfa_user(appengine_user):
    """ Retrieves the User object from the DB """
    return db.get(db.Key.from_path('User', appengine_user.user_id()))

def get_ordered_token(token_id):
    """ Retrieves the OrderedToken object from the DB """
    return db.get(db.Key.from_path('OrderedToken', token_id))


@app.route('/api/user', methods = ['PUT'])
def put_user():
    """ Creates a user. """
    appengine_user = users.get_current_user()
    if not appengine_user:
        abort(403)
    mfa_user = get_mfa_user(appengine_user)
    if mfa_user:
        abort(409)
    mfa_user = User(key_name = appengine_user.user_id(), email = appengine_user.email())
    mfa_user.put()
    return jsonify({'result':'CREATED'})


@app.route('/api/tokens', methods = ['GET'])
def get_tokens():
    """ Get all tokens for the logged-in user. """
    appengine_user = users.get_current_user()
    if not appengine_user:
        abort(403)
    
    mfa_user = get_mfa_user(appengine_user)
    if not mfa_user:
        abort(403)
    
    tokens = []
    for ordered_token_key in mfa_user.tokens:
        ordered_token = db.get(ordered_token_key)
        if not ordered_token:
            # TODO: log error, we have a data consistency problem
            abort(500)
        token = ordered_token.token
        if not token:
            # TODO: log error, we have a data consistency problem
            abort(500)
        tokens.append({ 'id': ordered_token.key().id_or_name(),
                        'order': ordered_token.order,
                        'name' : token.name,
                        'desc' : token.desc
        })
    return jsonify({ 'tokens': tokens} )


@app.route('/api/token', methods = ['PUT'])
def create_token():
    appengine_user = users.get_current_user()
    if not appengine_user:
        abort(403)
    if not request.json or not 'name' in request.json or not 'secret' in request.json:
        abort(400)
    mfa_user = get_mfa_user(appengine_user)
    if not mfa_user:
        abort(403)
    safe_name = cgi.escape(request.json['name'])
    if len(safe_name) > 254:
        abort(400)
    safe_desc = cgi.escape(request.json['desc'])
    if len(safe_desc) > 254:
        abort(400)
    secret = request.json['secret']
    if len(secret) != 16:
        abort(400)

    crypter = AES.new(SECRET_KEY, AES.MODE_ECB)
    token = Token(name = safe_name,
                  desc = safe_desc,
                  encrypted_private_key = crypter.encrypt(request.json['secret']),
                  owners = [db.Key.from_path('User', appengine_user.user_id())])
    token.put()
    ordered_token = OrderedToken(token = token.key(),
                                 order = -1)
    ordered_token.put()
    mfa_user.tokens.append(ordered_token.key())
    mfa_user.put()
    return jsonify({'result':'CREATED'})


@app.route('/api/token/<int:token_id>', methods = ['GET'])
def get_token_time_value(token_id):
    """ Get the OTP code for a given Token for the current time """
    appengine_user = users.get_current_user()
    if not appengine_user:
        abort(403)
    mfa_user = get_mfa_user(appengine_user)
    if not mfa_user:
        abort(403)
    ordered_token = get_ordered_token(token_id)
    if not ordered_token:
        abort(404)
    token = ordered_token.token
    if (mfa_user.key() not in token.owners) and (mfa_user.key() not in token.viewers):
        abort(404)
    crypter = AES.new(SECRET_KEY, AES.MODE_ECB)
    totp = TOTP(crypter.decrypt(token.encrypted_private_key))
    return jsonify({'code':totp.now()})
