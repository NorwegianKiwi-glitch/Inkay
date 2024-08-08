# db/my_db.py
import sqlite3

def create_connection():
    conn = sqlite3.connect('notater.db')
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS notater (
                notat TEXT
        )""")
    conn.commit()
    conn.close()

def insert_notat(notat):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO notater (notat) VALUES (?)", (notat,))
    conn.commit()
    conn.close()

# Initialize the database
if __name__ == "__main__":
    create_table()
