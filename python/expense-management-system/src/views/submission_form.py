from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models.database import Database

submission_form = Blueprint('submission_form', __name__)
db = Database()

@submission_form.route('/submit_expense', methods=['GET', 'POST'])
def submit_expense():
    if 'user_id' not in session:
        flash('Please log in to submit an expense.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        amount = request.form.get('amount', '').strip()
        description = request.form.get('description', '').strip()
        action = request.form.get('action', 'submit')

        if not amount or not description:
            flash('Amount and description are required!', 'danger')
            return redirect(url_for('submission_form.submit_expense'))

        status = 'Draft' if action == 'draft' else 'Pending'
        db.add_expense(
            user_id=session['user_id'],
            amount=amount,
            description=description,
            status=status
        )

        if status == 'Draft':
            flash('Expense saved as draft.', 'success')
            return redirect(url_for('drafts_view.view_drafts'))

        flash('Expense submitted successfully!', 'success')
        return redirect(url_for('expenses_view.my_expenses'))

    return render_template('submission_form.html')