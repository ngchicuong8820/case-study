import os
import subprocess
import hashlib
import sqlite3
from flask import Flask, request, send_file

app = Flask(__name__)

# =====================================================================
# THÀNH PHẦN 1: DATABASE (ĐÁP ỨNG TASK 5)
# =====================================================================
def init_db():
    """Khởi tạo cơ sở dữ liệu SQLite cho hệ thống E-commerce."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, tx_hash TEXT)''')
    conn.commit()
    conn.close()

# =====================================================================
# THÀNH PHẦN 2: EXTERNAL PAYMENT SERVICE (ĐÁP ỨNG TASK 5)
# (Giữ NGHIÊM NGẶT mã cũ từ app_high_1.py)
# =====================================================================
def get_cloud_credentials():
    # Lỗ hổng High: Lộ thông tin khóa bảo mật (Hardcoded AWS Keys)
    aws_access_key = "AKIAIOSFODNN7EXAMPLE"
    aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    return aws_access_key, aws_secret_key

def external_payment_gateway():
    """Mô phỏng gọi cổng thanh toán bên ngoài sử dụng khóa bí mật"""
    creds = get_cloud_credentials()
    return f"Connected to Payment Gateway using key: {creds[0]}"


# =====================================================================
# THÀNH PHẦN 3: WEB APP (ĐÁP ỨNG TASK 5)
# (Mở rộng từ app_medium_1.py nhưng giữ nguyên câu chào gốc)
# =====================================================================
@app.route("/")
def home():
    # Bao bọc câu chào gốc bằng giao diện HTML để trở thành Web App
    html_content = """
    <html>
        <head><title>E-commerce Web App</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>Welcome to the application.</h2>
            <p>Kiến trúc hệ thống bao gồm: Web App, API, Database (SQLite) và External Payment.</p>
        </body>
    </html>
    """
    return html_content


# =====================================================================
# THÀNH PHẦN 4: API SERVER (ĐÁP ỨNG TASK 5)
# (Giữ NGHIÊM NGẶT mã cũ từ app_critical, app_high_2 và app_medium_2)
# =====================================================================

# TỪ FILE: app_critical.py (API Chẩn đoán mạng)
@app.route("/network-test")
def ping_test():
    target_ip = request.args.get("ip", "8.8.8.8")
    # Lỗ hổng Critical: Thực thi lệnh OS trực tiếp từ tham số request
    command = f"ping -c 1 {target_ip}"
    output = subprocess.check_output(command, shell=True, text=True)
    
    return f"<pre>{output}</pre>"

# TỪ FILE: app_high_2.py (API Tải hóa đơn/tài liệu)
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

# TỪ FILE: app_medium_2.py (API Sinh mã băm cho giao dịch)
@app.route("/hash")
def generate_hash():
    user_data = request.args.get("data", "default_value")
    
    # Lỗ hổng Medium 2: Sử dụng hashlib.md5() 
    # Semgrep sẽ in ra log là: Severity: WARNING
    md5_hash = hashlib.md5(user_data.encode()).hexdigest()
    
    # Tích hợp thêm lưu vào Database để thể hiện logic E-commerce
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (tx_hash) VALUES (?)", (md5_hash,))
    conn.commit()
    conn.close()
    
    return f"MD5 Hash result: {md5_hash}"


# =====================================================================
# ENTRY POINT
# (Giữ NGHIÊM NGẶT mã cũ từ app_medium_1.py)
# =====================================================================
if __name__ == "__main__":
    # Khởi tạo CSDL khi chạy app
    init_db()
    
    # Lỗ hổng Medium 1: Kích hoạt chế độ debug (debug=True)
    # Semgrep sẽ in ra log là: Severity: WARNING
    app.run(host="0.0.0.0", port=8080, debug=True)