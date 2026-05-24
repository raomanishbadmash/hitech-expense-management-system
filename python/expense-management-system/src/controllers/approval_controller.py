from src.models.database import Database

class ApprovalController:
    def __init__(self):
        self.db = Database()

    def get_pending_expenses(self):
        return self.db.get_pending_expenses()

    def get_manager_approved_expenses(self):
        return self.db.get_manager_approved_expenses()

    def approve_expense(self, expense_id, role):
        expense = self.db.get_expense(expense_id)
        if not expense:
            return False

        if role in ['manager', 'admin'] and expense.status == 'Pending':
            expense.status = 'Manager Approved'
            self.db.update_expense(expense)
            return True

        return False

    def reject_expense(self, expense_id, role):
        expense = self.db.get_expense(expense_id)
        if not expense or role not in ['manager', 'admin']:
            return False

        if expense.status in ['Pending', 'Manager Approved']:
            expense.status = 'Rejected'
            self.db.update_expense(expense)
            return True

        return False

    def pay_expense(self, expense_id, role):
        expense = self.db.get_expense(expense_id)
        if not expense:
            return False

        if expense.status == 'Manager Approved' and role in ['finance', 'admin']:
            expense.status = 'Paid'
            self.db.update_expense(expense)
            return True

        return False
