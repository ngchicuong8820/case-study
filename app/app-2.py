from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/exec")
def execute():
    # Semgrep và CodeQL sẽ nhận diện đây là lỗi Critical (Remote Code Execution)
    cmd = request.args.get("cmd")
    return os.popen(cmd).read()