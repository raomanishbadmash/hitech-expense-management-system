from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models.database import Database

drafts_view = Blueprint('drafts_view', __name__)
db = Database()

@drafts_view.route('/drafts')
def view_drafts():
    if 'user_id' not in session:
        flash('Please log in to view drafts.', 'warning')
        return redirect(url_for('auth.login'))

    drafts = db.get_drafts_by_user(session['user_id'])
    return render_template('drafts.html', drafts=drafts)

@drafts_view.route('/drafts/submit/<int:draft_id>', methods=['POST'])
def submit_draft(draft_id):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    expense = db.get_expense(draft_id)
    if expense and expense.user_id == session['user_id'] and expense.status == 'Draft':
        expense.status = 'Pending'
        db.update_expense(expense)
        flash('Draft submitted successfully!', 'success')
    else:
        flash('Error submitting draft.', 'danger')
    return redirect(url_for('drafts_view.view_drafts'))

@drafts_view.route('/drafts/delete/<int:draft_id>', methods=['POST'])
def delete_draft(draft_id):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    success = db.delete_draft(draft_id, user_id=session['user_id'])
    if success:
        flash('Draft deleted successfully.', 'success')
    else:
        flash('Error deleting draft.', 'danger')
    return redirect(url_for('drafts_view.view_drafts'))