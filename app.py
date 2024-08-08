from flask import Flask, render_template, request, redirect, url_for
from db.my_db import insert_notat, create_table  # Corrected import statement

app = Flask(__name__)

# Ensure the table is created when the app starts
create_table()

@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    if request.method == "POST":
        notat = request.form["notat"]
        insert_notat(notat)
        return redirect(url_for('index'))
    return render_template("index.html")

if __name__ == '__main__':
	app.run(debug=True)