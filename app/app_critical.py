from flask import Flask, request
import urllib.request

app = Flask(__name__)

# Lỗi High 1: Lộ thông tin khóa bí mật (Hardcoded API Key / Secret)
SECRET_API_KEY = "AKIAIOSFODNN7EXAMPLE"

@app.route("/")
def home():
    target_url = request.args.get("url")
    if target_url:
        response = urllib.request.urlopen(target_url)
        return response.read()
    return f"Home page. API Key configured: {SECRET_API_KEY[:5]}..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)