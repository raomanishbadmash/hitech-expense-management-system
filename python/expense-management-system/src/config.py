DATABASE_URI = "sqlite:///expense_management.db"
SECRET_KEY = "your_secret_key_here"
DEBUG = True

# Role definitions
ROLES = {
    "Admin": {
        "permissions": ["manage_users", "approve_expenses", "view_reports"]
    },
    "Manager": {
        "permissions": ["approve_expenses", "view_reports"]
    },
    "User": {
        "permissions": ["submit_expenses", "view_own_expenses"]
    }
}