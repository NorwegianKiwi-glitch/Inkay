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
                header TEXT,
                notat TEXT
        )""")
    conn.commit()
    conn.close()

def insert_notat(header, notat):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO notater (header, notat) VALUES (?, ?)", (header, notat))
    conn.commit()
    conn.close()

def get_all_headers():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT header FROM notater")
    headers = c.fetchall()
    conn.close()
    return headers

if __name__ == "__main__":
    create_table()
