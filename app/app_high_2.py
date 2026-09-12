from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route("/download")
def download_file():
    # Lỗ hổng High 2: Path Traversal (Directory Traversal)
    # Không kiểm tra đầu vào, cho phép kẻ tấn công thoát khỏi thư mục chỉ định
    file_name = request.args.get("file", "default.txt")
    
    base_dir = "/var/www/app/downloads"
    file_path = os.path.join(base_dir, file_name)
    
    if os.path.exists(file_path):
        return send_file(file_path)
    return "File not found", 404