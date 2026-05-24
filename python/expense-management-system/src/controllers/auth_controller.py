from flask import request, jsonify, session
from src.models.user import User
from src.models.database import Database

class AuthController:
    def __init__(self):
        self.db = Database()

    def login(self):
        username = request.json.get('username')
        password = request.json.get('password')
        user = self.db.get_user_by_username(username)

        if user and user.verify_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            return jsonify({"message": "Login successful", "role": user.role}), 200
        return jsonify({"message": "Invalid username or password"}), 401

    def logout(self):
        session.clear()
        return jsonify({"message": "Logout successful"}), 200

    def get_current_user(self):
        user_id = session.get('user_id')
        if user_id:
            user = self.db.get_user_by_id(user_id)
            return jsonify({"username": user.username, "role": user.role}), 200
        return jsonify({"message": "No user logged in"}), 401

    def is_admin(self):
        return session.get('role') == 'Admin'

    def is_manager(self):
        return session.get('role') == 'Manager'

    def is_user(self):
        return session.get('role') == 'User'