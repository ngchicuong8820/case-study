from flask import Flask, request
import os

app = Flask(__name__)

# Lỗi cố ý: Hardcoded API Key cho Semgrep phát hiện
API_KEY = "AKIAIOSFODNN7EXAMPLE" 

@app.route("/")
def home():
    return "DevSecOps Lab Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)