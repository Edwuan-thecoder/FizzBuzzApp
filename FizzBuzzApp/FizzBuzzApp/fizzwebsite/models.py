# importing from the current package
from . import db
# import class to help keep track of current User
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Records(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    user_inputs = db.Column(db.Integer, primary_key=True)
    amount_of_inputs = db.Column(db.Integer)

