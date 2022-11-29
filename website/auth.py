"""
auth.py is used to create authentication of user.
In this we route all pages which is related to authentication.
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

"""
A Blueprint is a way to organize a group of related views and other code. Rather than registering views and 
other code directly with an application, they are registered with a blueprint. Then the blueprint is registered 
with the application when it is available in the factory function.
"""
auth = Blueprint('auth', __name__)


# the route() decorator to tell Flask what URL should trigger our function.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect, try again', category='error')
        else:
            flash('Email not found please sign up first...', category="error")


    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user and user.is_active:
            flash("Email already exists", category="error")
        elif len(email) < 4:
            flash("Email must be 3 characres", category="error")
        elif len(first_name) < 2:
            flash("first name must be a single character", category="error")
        elif (password1 != password2):
            flash("password don\'t match", category="error")
        elif len(password1) < 7:
            flash("password must be more than 6 characters", category="error")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash("user created", category="success")
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
