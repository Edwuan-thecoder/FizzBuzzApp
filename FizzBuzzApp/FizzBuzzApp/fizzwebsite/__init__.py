import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey_edwuan'

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)
db.init_app(app)
from .models import User
db.create_all()

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()
# can now pass in our app to the login manager
login_manager.init_app(app)
# Tell users what view to go to when they need to login.
login_manager.login_view = "auth.login"

# looking for the User table and reference them by their id
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

###########################
#### BLUEPRINT CONFIGS #######
#########################

# We've imported them here for easy reference
from .views import views
from .auth import auth


# Register the apps
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix="/")
# app.register_blueprint(error_pages)