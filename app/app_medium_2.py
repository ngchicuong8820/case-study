import hashlib
from flask import Flask, request

app = Flask(__name__)

@app.route("/hash")
def generate_hash():
    user_data = request.args.get("data", "default_value")
    
    # Lỗ hổng Medium 2: Sử dụng hashlib.md5() 
    # Semgrep sẽ in ra log là: Severity: WARNING
    md5_hash = hashlib.md5(user_data.encode()).hexdigest()
    
    return f"MD5 Hash result: {md5_hash}"