from flask import Flask, render_template, request, redirect, url_for
from db.my_db import insert_notat, create_table

app = Flask(__name__)

# Ensure the table is created when the app starts
create_table()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        header = request.form["header"]
        notat = request.form["notat"]
        insert_notat(header, notat)
        return redirect(url_for('index'))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
