from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
import sqlalchemy
# import flask login to have the ability to hash a password
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # retrieve data from frontend
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Using RAW SQL to query the database for email and password
        user = db.engine.execute(f"SELECT * FROM User WHERE email = '{email}'").first()
        # user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category="success")

                user = User.query.filter_by(email=email).first()
                # Use login user so the User will not have to log in every single time
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required  # Make sure that the User could only logout if they were already logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():
    # Retrieving data from frontend and checking to make sure all User Login data is valid
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist.', category='error')
        else:
            if len(email) < 4:
                flash("Email must be greater than 3 characters.", category='error')

            elif len(first_name) < 2:
                flash("First name must be greater than 1 character.", category='error')
            elif password1 != password2:
                flash("Passwords don\'t match.", category='error')
            elif len(password1) < 7:
                flash("Password must be at least 7 characters.", category='error')
            else:
                # add user to database
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)

                db.session.commit()
                # Use login user so the User will not have to log in every single time
                # login_user(user, remember=True)
                flash("Account created!", category='success')
                # take the User back to the home page after we signed uo
                return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)