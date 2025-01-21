from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.models import User
from models.conn import db

auth = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return redirect(url_for('auth.login', error='Please check your login details and try again.'))
        
        login_user(user, remember=remember)
        
        return redirect(url_for('auth.profile'))
    
    error = request.args.get('error')
    message = request.args.get('message')
    return render_template('login.html', error=error, message=message)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            print(username, email, password, confirm_password)
            return redirect(url_for('auth.signup', error='Please fill out all fields.'))
        
        if password != confirm_password:
            return redirect(url_for('auth.signup', error='The passwords do not match.'))

        user = User.query.filter_by(email=email).first()
        if user:
            return redirect(url_for('auth.signup', error='User with this email address already exists.'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login', message='Registration successful! You can now log in.'))

    error = request.args.get('error')
    return render_template('signup.html', error=error)

# Uncomment and modify if you need an admin dashboard
# @auth.route('/admin_dashboard')
# @login_required
# def admin_dashboard():
#     if not current_user.has_role('admin'):
#         flash('Unauthorized access!')
#         return redirect(url_for('auth.profile'))
#     return render_template('admin_dashboard.html')
