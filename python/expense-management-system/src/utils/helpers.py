def calculate_total_expenses(expenses):
    return sum(expense['amount'] for expense in expenses)

def format_currency(amount):
    return "${:,.2f}".format(amount)

def validate_expense_data(expense_data):
    required_fields = ['amount', 'description']
    for field in required_fields:
        if field not in expense_data:
            return False, f"Missing required field: {field}"
    return True, "Validation successful"

def get_user_role(user):
    return user.role if user else None

def is_admin(user):
    return user.role == 'Admin'

def is_manager(user):
    return user.role == 'Manager'