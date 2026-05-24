from flask import Blueprint, render_template, session, redirect, url_for, flash
from src.models.database import Database

expenses_view = Blueprint('expenses_view', __name__)
db = Database()

@expenses_view.route('/my_expenses')
def my_expenses():
    if 'user_id' not in session:
        flash('Please log in to view your expenses.', 'warning')
        return redirect(url_for('auth.login'))

    expenses = db.get_expenses_by_user(session['user_id'])
    return render_template('my_expenses.html', expenses=expenses)

@expenses_view.route('/expense/<int:expense_id>')
def view_expense(expense_id):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    expense = db.get_expense(expense_id)
    if expense and expense.user_id == session['user_id']:
        return render_template('view_expense.html', expense=expense)
    else:
        flash('Expense not found', 'danger')
        return redirect(url_for('expenses_view.my_expenses'))