from flask import Flask, request
import urllib.request

app = Flask(__name__)

# Lỗi: Hardcoded Secret (Semgrep, Trivy Secret, SonarQube bắt được)
API_KEY = "AKIAIOSFODNN7EXAMPLE" 

@app.route("/")
def home():
    # Lỗi: SSRF (Server-Side Request Forgery) do nhận trực tiếp URL từ user
    target_url = request.args.get("url")
    if target_url:
        response = urllib.request.urlopen(target_url)
        return response.read()
    return "DevSecOps Lab Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)