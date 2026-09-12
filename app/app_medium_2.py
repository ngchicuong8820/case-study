from flask import Flask, request
import hashlib

app = Flask(__name__)

@app.route("/hash")
def hash_data():
    data = request.args.get("data", "default_value")
    
    # Lỗ hổng Medium 2: Sử dụng MD5 - thuật toán băm mật mã lỗi thời và yếu
    hash_object = hashlib.md5(data.encode())
    
    return f"MD5 Hash: {hash_object.hexdigest()}"