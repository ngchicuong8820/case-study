from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/login")
def login():
    username = request.args.get("user", "")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Lỗi: SQL Injection nghiêm trọng (Semgrep, CodeQL, SonarQube bắt lập tức)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.executescript(query)

    return "Login check executed."