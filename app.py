from flask import Flask, render_template, request, redirect, url_for
from db.my_db import insert_notat, create_table, get_all_headers

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

    # Get all headers from the database
    headers = get_all_headers()
    
    # Pass headers to the template
    return render_template("index.html", headers=headers)

@app.route("/test")
def test():
    return("Oscar morhterfuckings Godtland")

if __name__ == "__main__":
    app.run(debug=True)
