from ..models.database import Database

class ExpenseController:
    def __init__(self):
        self.db = Database()

    def submit_expense(self, user_id, amount, description, status='Draft'):
        return self.db.add_expense(user_id=user_id, amount=amount, description=description, status=status)

    def get_user_expenses(self, user_id):
        return self.db.get_expenses_by_user(user_id)

    def get_user_drafts(self, user_id):
        return self.db.get_drafts_by_user(user_id)

    def get_expense(self, expense_id):
        return self.db.get_expense(expense_id)

    def approve_expense(self, expense_id):
        expense = self.db.get_expense(expense_id)
        if expense:
            expense.status = 'Approved'
            self.db.update_expense(expense)
            return True
        return False

    def reject_expense(self, expense_id):
        expense = self.db.get_expense(expense_id)
        if expense:
            expense.status = 'Rejected'
            self.db.update_expense(expense)
            return True
        return False