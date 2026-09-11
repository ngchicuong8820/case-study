from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/exec")
def execute_command():
    # Lỗi: Remote Code Execution / Command Injection (Semgrep & CodeQL bắt buộc phải phát hiện)
    cmd = request.args.get("cmd", "whoami")
    output = os.popen(cmd).read()
    return f"<pre>{output}</pre>"