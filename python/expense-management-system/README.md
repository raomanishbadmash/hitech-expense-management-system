# Expense Management System (ETM)

## Overview
The Expense Management System (ETM) is a Python-based application designed to streamline the process of expense submission, approval, and management. It supports multiple user roles, including Admin, Manager, and User, each with specific permissions and functionalities.

## Features
- **User Login**: Secure login functionality with three different roles: Admin, Manager, and User.
- **Expense Submission**: Users can submit their expenses through a dedicated form.
- **My Drafts**: Users can view and manage their draft submissions before finalizing them.
- **My Expenses**: A screen for users to view their submitted expenses and their statuses.
- **Expense Approver Screen**: Admins and Managers can review and approve submitted expenses.
- **Approval Workflow**: Users submit expenses, which are then approved by their assigned managers.

## Project Structure
```
expense-management-system
├── src
│   ├── main.py
│   ├── config.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── login.py
│   │   └── roles.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── expense.py
│   │   └── database.py
│   ├── views
│   │   ├── __init__.py
│   │   ├── login_view.py
│   │   ├── submission_form.py
│   │   ├── drafts_view.py
│   │   ├── expenses_view.py
│   │   └── approver_view.py
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── expense_controller.py
│   │   └── approval_controller.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/expense-management-system.git
   ```
2. Navigate to the project directory:
   ```
   cd expense-management-system
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/main.py
   ```
2. Access the application in your web browser at `http://localhost:5000`.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.