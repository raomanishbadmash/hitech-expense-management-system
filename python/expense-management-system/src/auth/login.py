from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from ..models.database import Database

login_blueprint = Blueprint('auth', __name__)

db = Database()


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db.get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')



@login_blueprint.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))