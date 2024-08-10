# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from db.my_db import create_user, get_user_by_username, check_user_password, create_table, insert_notat, create_table, get_all_headers, get_notat_by_id, update_notat, delete_notat

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Ensure the table is created when the app starts
create_table()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get(username):
        user = get_user_by_username(username)
        if user:
            return User(user[0], user[1])
        return None

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_username(user_id)
    if user:
        return User(user[0], user[1])
    return None

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = create_user(username, password)
        if result == "User created successfully.":
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        else:
            flash(result)
            return redirect(url_for('register'))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = check_user_password(username, password)
        if user:
            user_obj = User(user[0], user[1])
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
# @login_required
def index():
    if request.method == "POST":
        header = request.form["header"]
        notat = request.form["notat"]
        result = insert_notat(header, notat)
        if result == "Header cannot be empty.":
            flash(result)
            return redirect(url_for('index'))

        return redirect(url_for('index'))

    headers = get_all_headers()
    return render_template("index.html", headers=headers)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        header = request.form["header"]
        notat = request.form["notat"]
        result = update_notat(id, header, notat)
        if result == "Header cannot be empty.":
            flash(result)
            return redirect(url_for('edit', id=id))

        return redirect(url_for('index'))

    notat_data = get_notat_by_id(id)
    headers = get_all_headers()  # Fetch headers to display in the edit page
    return render_template("edit.html", notat_data=notat_data, headers=headers)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    delete_notat(id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
