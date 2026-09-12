from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/login")
def login():
    username = request.args.get("user", "")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Lỗi High 2: Lối ghép chuỗi SQL trực tiếp qua f-string gây SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    return "Login check executed."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)