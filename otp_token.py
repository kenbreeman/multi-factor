from google.appengine.ext import db
 
class Token(db.Model):
    name = db.StringProperty(required=True)
    desc = db.StringProperty(required=True)
    encrypted_private_key = db.StringProperty(required=True)
    # List of User
    owners = db.ListProperty(db.Key)
    # List of User
    viewers = db.ListProperty(db.Key)
 
 
class OrderedToken(db.Model):
    token = db.ReferenceProperty(Token)
    order = db.IntegerProperty()
