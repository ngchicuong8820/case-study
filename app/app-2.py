from flask import Flask, request, render_template_string
import os
import subprocess

app = Flask(__name__)

# Cố tình đặt hardcoded secret để Semgrep, SonarQube và Trivy (secret scan) phát hiện
API_KEY = "AKIAIOSFODNN7EXAMPLE" 
DB_PASSWORD = "SuperSecretPassword123!"

@app.route("/")
def home():
    return """
    <h1>DevSecOps Lab Running!</h1>
    <p>Welcome to the vulnerable test application.</p>
    <ul>
        <li><a href="/vulnerable-exec?cmd=echo">Test Command Execution</a></li>
        <li><a href="/search?q=test">Test Search Page</a></li>
    </ul>
    """

# Route cố tình dính lỗi Command Injection để SAST và DAST (OWASP ZAP) phát hiện
@app.route("/vulnerable-exec")
def vulnerable_exec():
    cmd = request.args.get("cmd", "ls")
    # Lỗ hổng bảo mật: sử dụng trực tiếp input từ người dùng vào lệnh hệ thống
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        return f"<pre>{output}</pre>"
    except Exception as e:
        return f"Error: {str(e)}", 500

# Route mô phỏng lỗi XSS để OWASP ZAP phát hiện
@app.route("/search")
def search():
    query = request.args.get("q", "")
    # Lỗ hổng XSS phản chiếu (Reflected XSS) do không sanitize input
    template = f"<h1>Search Results for: {query}</h1>"
    return render_template_string(template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)