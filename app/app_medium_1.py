from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the application."

if __name__ == "__main__":
    # Lỗ hổng Medium 1: Kích hoạt chế độ debug (debug=True)
    # Semgrep sẽ in ra log là: Severity: WARNING
    app.run(host="0.0.0.0", port=8080, debug=True)