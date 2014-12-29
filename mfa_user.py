from google.appengine.ext import db
 
class User(db.Model):
    email = db.StringProperty(required=True)
    # List of OrderedToken
    tokens = db.ListProperty(db.Key)
