import os
import subprocess
import hashlib
import sqlite3
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

# =====================================================================
# SYSTEM INITIALIZATION
# =====================================================================
def init_db():
    """Khởi tạo cơ sở dữ liệu cho hệ thống E-commerce."""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# =====================================================================
# CLOUD INTEGRATION (LỖI HIGH 1 - HARDCODED SECRETS)
# =====================================================================
def upload_invoice_to_s3(file_path):
    """
    Hàm nội bộ để đồng bộ hóa hóa đơn (PDF) lên AWS S3 storage.
    [VULNERABILITY]: Lộ lọt khóa truy cập môi trường Cloud. Trivy fs sẽ đánh rớt pipeline.
    """
    aws_access_key = "AKIAIOSFODNN7EXAMPLE"
    aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    # Giả lập logic upload
    print(f"Uploading {file_path} to S3 using token {aws_access_key}...")
    return True

# =====================================================================
# API ENDPOINTS
# =====================================================================

@app.route('/api/v1/auth/legacy-login', methods=['POST'])
def legacy_login():
    """
    API xác thực người dùng cho các hệ thống cũ.
    [LỖI MEDIUM 1 - WEAK CRYPTOGRAPHY]: Semgrep sẽ cảnh báo thuật toán băm yếu.
    """
    username = request.form.get('username')
    password = request.form.get('password', '')

    # Sử dụng MD5 để băm mật khẩu thay vì bcrypt hoặc Argon2
    password_hash = hashlib.md5(password.encode()).hexdigest()

    if username == "admin" and password_hash == "5f4dcc3b5aa765d61d8327deb882cf99":
        return jsonify({"status": "success", "token": "jwt-token-12345"}), 200
    
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.route('/api/v1/invoices/download', methods=['GET'])
def download_invoice():
    """
    API cho phép khách hàng tải xuống hóa đơn điện tử (PDF).
    [LỖI HIGH 2 - PATH TRAVERSAL]: SonarCloud & Semgrep sẽ báo cáo lỗi truyền dữ liệu bẩn.
    """
    invoice_file = request.args.get("file_name")
    if not invoice_file:
        return jsonify({"error": "Missing file_name parameter"}), 400
    
    # Không sanitize input, cho phép truyền ../../ để đọc file cấu hình hệ thống
    base_dir = "/var/www/app/data/invoices/"
    target_path = os.path.join(base_dir, invoice_file)
    
    if os.path.exists(target_path):
        upload_invoice_to_s3(target_path) # Kích hoạt tính năng backup
        return send_file(target_path)
    
    return jsonify({"error": "Invoice not found"}), 404


@app.route('/api/v1/admin/diagnostics/network', methods=['GET'])
def network_diagnostics():
    """
    API dành cho Admin để kiểm tra kết nối mạng tới Cổng thanh toán (External Payment Gateway).
    [LỖI CRITICAL 1 - OS COMMAND INJECTION]: Điểm yếu chết người cho phép chiếm quyền máy chủ.
    """
    # Trong thực tế cần có token JWT của admin ở đây, nhưng mô phỏng đang bị thiếu (Broken Access Control)
    target_ip = request.args.get("ip", "api.stripe.com")
    
    # Lấy đầu vào từ request và ném trực tiếp vào shell hệ thống
    command = f"ping -c 1 {target_ip}"
    
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return f"<h3>Diagnostic Result:</h3><pre>{output}</pre>", 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Network diagnostic failed", "details": str(e)}), 500


# =====================================================================
# APPLICATION ENTRY POINT
# =====================================================================
if __name__ == '__main__':
    init_db()
    # [LỖI MEDIUM 2 - DEBUG MODE ENABLED]: Để lộ thông tin runtime trên production
    app.run(host='0.0.0.0', port=8080, debug=True)