from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from db.my_db import create_user, get_user_by_username, check_user_password, create_table, insert_notat, create_table, get_all_headers, get_notat_by_id, update_notat, delete_notat, check_password_hash, create_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Ensure the table is created when the app starts
create_table()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# login_manager.debug = True  # Enable debug mode

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

    def get_id(self):
        return str(self.id)  # Ensure this returns the user ID as a string

def check_user_password(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user[2], password):
        return user
    return None

@login_manager.user_loader
def load_user(user_id):
    print(f"Loading user with ID: {user_id}")
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        print(f"User found: {user}")
        return User(user[0], user[1])
    print("No user found")
    return None


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = create_user(username, password)
        if result == "User created successfully.":
            flash("Registration successful! Please log in.")
            print("Registration successful")
            return redirect(url_for('login'))
        else:
            flash(result)
            print("Registration failed")
            return redirect(url_for('register'))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = check_user_password(username, password)
        if user:
            user_obj = User(user[0], user[1])  # Ensure user[0] is the ID and user[1] is the username
            login_user(user_obj)  # Ensure this is being called correctly
            print("Login successful")
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
@login_required
def index():
    print(f"Current user: {current_user}")

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
@login_required
def edit(id):
    print(f"Current user: {current_user}")

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
@login_required
def delete(id):
    delete_notat(id)
    return redirect(url_for('index'))

@app.route("/debug-session")
def debug_session():
    return f"Session: {session}"

if __name__ == "__main__":
    app.run(debug=True)
