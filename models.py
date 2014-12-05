from google.appengine.ext import db

class Review(db.Model):
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now=True)
    hotel_name = db.StringProperty(multiline=True)
    numeric_rating = db.StringProperty(multiline=True)
    
