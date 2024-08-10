# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from db.my_db import insert_notat, create_table, get_all_headers, get_notat_by_id, update_notat, delete_notat

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Ensure the table is created when the app starts
create_table()

@app.route("/", methods=["GET", "POST"])
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
