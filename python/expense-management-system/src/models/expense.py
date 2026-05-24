class Expense:
    def __init__(self, amount, description, status='Draft'):
        self.amount = amount
        self.description = description
        self.status = status

    def submit(self):
        self.status = 'Submitted'

    def approve(self):
        self.status = 'Approved'

    def reject(self):
        self.status = 'Rejected'

    def __str__(self):
        return f'Expense(amount={self.amount}, description="{self.description}", status="{self.status}")'