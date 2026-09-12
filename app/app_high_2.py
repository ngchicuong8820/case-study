import os
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route("/download")
def download_document():
    # Lỗ hổng High: Đọc file hệ thống trái phép (Directory Traversal)
    file_name = request.args.get("file_name")
    
    # Không sanitize input, ghép chuỗi trực tiếp vào đường dẫn
    base_dir = "/var/www/app/data/"
    target_path = os.path.join(base_dir, file_name)
    
    if os.path.exists(target_path):
        return send_file(target_path)
    return "File not found", 404