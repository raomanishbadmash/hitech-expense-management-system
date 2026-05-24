from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.controllers.approval_controller import ApprovalController

approver_view = Blueprint('approver_view', __name__)
approval_controller = ApprovalController()

@approver_view.route('/approvals', methods=['GET'])
def view_approvals():
    if 'user_id' not in session:
        flash('Please log in to view approvals.', 'warning')
        return redirect(url_for('auth.login'))

    if session.get('role') not in ['manager', 'admin']:
        flash('Approvals are only available to managers or administrators.', 'warning')
        return redirect(url_for('home'))

    expenses = approval_controller.get_pending_expenses()
    return render_template('approvals.html', expenses=expenses, role=session.get('role'))

@approver_view.route('/payments', methods=['GET'])
def view_payments():
    if 'user_id' not in session:
        flash('Please log in to view payment queue.', 'warning')
        return redirect(url_for('auth.login'))

    if session.get('role') not in ['finance', 'admin']:
        flash('Payments are only available to finance or administrators.', 'warning')
        return redirect(url_for('home'))

    expenses = approval_controller.get_manager_approved_expenses()
    return render_template('payments.html', expenses=expenses, role=session.get('role'))

@approver_view.route('/approve/<int:expense_id>', methods=['POST'])
def approve_expense(expense_id):
    if session.get('role') not in ['manager', 'admin']:
        flash('You are not allowed to approve expenses.', 'danger')
        return redirect(url_for('home'))

    result = approval_controller.approve_expense(expense_id, session.get('role'))
    if result:
        flash('Expense approved successfully!', 'success')
    else:
        flash('Failed to approve expense.', 'danger')
    return redirect(url_for('approver_view.view_approvals'))

@approver_view.route('/reject/<int:expense_id>', methods=['POST'])
def reject_expense(expense_id):
    if session.get('role') not in ['manager', 'admin']:
        flash('You are not allowed to reject expenses.', 'danger')
        return redirect(url_for('home'))

    result = approval_controller.reject_expense(expense_id, session.get('role'))
    if result:
        flash('Expense rejected successfully!', 'success')
    else:
        flash('Failed to reject expense.', 'danger')
    return redirect(url_for('approver_view.view_approvals'))

@approver_view.route('/pay/<int:expense_id>', methods=['POST'])
def pay_expense(expense_id):
    if session.get('role') not in ['finance', 'admin']:
        flash('You are not allowed to pay expenses.', 'danger')
        return redirect(url_for('home'))

    result = approval_controller.pay_expense(expense_id, session.get('role'))
    if result:
        flash('Expense marked as paid successfully!', 'success')
    else:
        flash('Failed to mark expense as paid.', 'danger')
    return redirect(url_for('approver_view.view_payments'))
