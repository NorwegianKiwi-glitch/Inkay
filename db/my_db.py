# db/my_db.py
import sqlite3
import os

def create_connection():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../instance/notater.db'))
    
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))

    conn = sqlite3.connect(db_path)
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS notater (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                header TEXT,
                notat TEXT
        )""")
    conn.commit()
    conn.close()

def insert_notat(header, notat):
    if not header.strip():  # Check if the header is empty or only whitespace
        return "Header cannot be empty."

    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO notater (header, notat) VALUES (?, ?)", (header, notat))
    conn.commit()
    conn.close()

def get_all_headers():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT id, header FROM notater")
    headers = c.fetchall()
    conn.close()
    return headers

def get_notat_by_id(id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM notater WHERE id = ?", (id,))
    notat_data = c.fetchone()
    conn.close()
    return notat_data

def update_notat(id, header, notat):
    if not header.strip():  # Check if the header is empty or only whitespace
        return "Header cannot be empty."

    conn = create_connection()
    c = conn.cursor()
    c.execute("UPDATE notater SET header = ?, notat = ? WHERE id = ?", (header, notat, id))
    conn.commit()
    conn.close()

def delete_notat(id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM notater WHERE id = ?", (id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
