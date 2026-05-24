from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Expense(Base):
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default='Pending')

DATABASE_URL = 'sqlite:///expenses.db'  # Example for SQLite, change as needed
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)

SessionFactory = sessionmaker(bind=engine)
session = scoped_session(SessionFactory)


def create_user_if_missing(username, password, role):
    if not session.query(User).filter_by(username=username).first():
        user = User(username=username, password=generate_password_hash(password), role=role)
        session.add(user)
        session.commit()


def create_default_users():
    create_user_if_missing('employee', 'password', 'user')
    create_user_if_missing('manager', 'password', 'manager')
    create_user_if_missing('finance', 'password', 'finance')
    create_user_if_missing('admin', 'password', 'admin')


create_default_users()


class Database:
    """Simple database helper wrapping the SQLAlchemy session and mapped models."""

    def __init__(self):
        self.session = session

    def add_expense(self, user_id, amount, description, status='Pending'):
        mapped = Expense(
            user_id=user_id,
            amount=float(amount),
            description=description,
            status=status
        )
        self.session.add(mapped)
        self.session.commit()
        return mapped

    def get_user_by_username(self, username):
        return self.session.query(User).filter_by(username=username).first()

    def create_user(self, username, password, role='user'):
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password, role=role)
        self.session.add(user)
        self.session.commit()
        return user

    def get_expenses_by_user(self, user_id):
        return self.session.query(Expense).filter_by(user_id=user_id).all()

    def get_drafts_by_user(self, user_id):
        return self.session.query(Expense).filter_by(user_id=user_id, status='Draft').all()

    def get_expense(self, expense_id):
        return self.session.query(Expense).filter_by(id=expense_id).first()

    def get_pending_expenses(self):
        return self.session.query(Expense).filter_by(status='Pending').all()

    def get_manager_approved_expenses(self):
        return self.session.query(Expense).filter_by(status='Manager Approved').all()

    def get_expenses_by_status(self, status):
        return self.session.query(Expense).filter_by(status=status).all()

    def update_expense(self, expense):
        self.session.merge(expense)
        self.session.commit()
        return expense

    def delete_draft(self, draft_id, user_id):
        obj = self.session.query(Expense).filter_by(id=draft_id, status='Draft', user_id=user_id).first()
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True