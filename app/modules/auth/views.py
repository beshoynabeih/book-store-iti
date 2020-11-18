from flask import Blueprint, request, render_template, redirect, url_for, flash
from .models import User
from app import bcrypt, db
from flask_login import login_user, logout_user, current_user

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

@auth_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))
    if request.method == 'POST':
        user_data = request.form
        if user_data["email"] and user_data["password"]:
            user = User.query.filter_by(email=user_data["email"]).first()
            if user and bcrypt.check_password_hash(user.password, user_data["password"]):
                login_user(user)
                return redirect(url_for('movies.index'))
            else:
                flash('Username or password is incorrect', 'danger')
                return render_template('auth/login.html')
        flash('Username and password is required', 'danger')
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@auth_blueprint.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))
    if request.method == 'POST':
        user_data = request.form
        print(user_data)
        if user_data["username"] and user_data["email"] and user_data["password"] and user_data["confirm_password"]:
            if user_data["password"] == user_data["confirm_password"]:
                user = User(username=user_data["username"], email=user_data["email"])
                user.password = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')
                db.session.add(user)
                db.session.commit()
                flash('Congratulations! Welcome onboard')
                return redirect(url_for('movies.index'))

        return render_template('auth/register.html')
    else:
        return render_template('auth/register.html')

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('movies.index'))