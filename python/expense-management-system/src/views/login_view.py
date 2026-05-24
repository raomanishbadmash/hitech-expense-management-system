from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.auth.login import authenticate_user

login_view = Blueprint('login_view', __name__)

@login_view.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = authenticate_user(username, password)
        
        if role:
            # Here you would typically set the user session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to a home or dashboard page
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')  # Render the login template