import sys
from pathlib import Path

# Ensure project root is on sys.path so imports like `from src...` work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ast

# Compatibility shim for Python 3.14+ where ast.Str/Num were removed.
# Provide minimal AST node classes that Werkzeug expects (they must
# subclass ast.AST and include lineno/col offsets so compile() succeeds).
if not hasattr(ast, "Str"):
    class _Str(ast.Constant):
        def __init__(self, s):
            try:
                super().__init__(value=s)
            except TypeError:
                self.value = s
            self.s = s
            self.lineno = 1
            self.col_offset = 0
            self.end_lineno = 1
            self.end_col_offset = 0
    ast.Str = _Str

if not hasattr(ast, "Num"):
    class _Num(ast.Constant):
        def __init__(self, n):
            try:
                super().__init__(value=n)
            except TypeError:
                self.value = n
            self.n = n
            self.lineno = 1
            self.col_offset = 0
            self.end_lineno = 1
            self.end_col_offset = 0
    ast.Num = _Num

if not hasattr(ast, "NameConstant"):
    class _NameConstant(ast.Constant):
        def __init__(self, value):
            try:
                super().__init__(value=value)
            except TypeError:
                self.value = value
            self.lineno = 1
            self.col_offset = 0
            self.end_lineno = 1
            self.end_col_offset = 0
    ast.NameConstant = _NameConstant

if not hasattr(ast, "Bytes"):
    class _Bytes(ast.Constant):
        def __init__(self, b: bytes):
            try:
                super().__init__(value=b)
            except TypeError:
                self.value = b
            self.s = b
            self.lineno = 1
            self.col_offset = 0
            self.end_lineno = 1
            self.end_col_offset = 0
    ast.Bytes = _Bytes

from flask import Flask, render_template, session, redirect, url_for
from src.auth.login import login_blueprint
from src.views.submission_form import submission_form
from src.views.drafts_view import drafts_view
from src.views.expenses_view import expenses_view
from src.views.approver_view import approver_view
from src.models.database import session as db_session

app = Flask(
    __name__,
    template_folder=str(Path(__file__).resolve().parent / 'templates'),
    static_folder=str(Path(__file__).resolve().parent / 'static')
)
app.secret_key = 'replace-with-a-secure-secret'

# Register blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(submission_form)
app.register_blueprint(drafts_view)
app.register_blueprint(expenses_view)
app.register_blueprint(approver_view)

@app.teardown_appcontext
def remove_session(exception=None):
    db_session.remove()

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from src.models.database import Database
    db = Database()
    user_id = session.get('user_id')
    
    # Get live data
    all_expenses = [e for e in db.get_expenses_by_user(user_id) if e.status != 'Draft']
    drafts = db.get_drafts_by_user(user_id)
    pending = [e for e in all_expenses if e.status == 'Pending']
    
    return render_template('home.html', 
                         total_expenses=len(all_expenses),
                         total_drafts=len(drafts),
                         total_pending=len(pending))

if __name__ == '__main__':
    app.run(debug=True)