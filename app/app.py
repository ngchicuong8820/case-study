import os
import subprocess
import hashlib
import sqlite3
from flask import Flask, request, send_file, jsonify, render_template_string

app = Flask(__name__)

# =====================================================================
# 1. DATABASE COMPONENT & INITIALIZATION
# =====================================================================
def init_db():
    """Khởi tạo Database SQLite cho ứng dụng"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    # Thêm user admin mặc định (password lưu dạng hash MD5 của chữ 'admin123')
    cursor.execute("INSERT INTO users (username, password) SELECT 'admin', '0192023a7bbd73250516f069df18b500' WHERE NOT EXISTS(SELECT 1 FROM users WHERE username='admin')")
    conn.commit()
    conn.close()

# =====================================================================
# 2. EXTERNAL PAYMENT SERVICE COMPONENT
# =====================================================================
# [LỖI HIGH 1: Hardcoded Secrets] - Trivy sẽ chặn vì lộ API Key của Stripe
STRIPE_SECRET_KEY = "sk_live_51Mabcde1234567890XYZ"

def process_external_payment(amount):
    """Mô phỏng gọi API sang cổng thanh toán bên ngoài"""
    print(f"Connecting to External Payment Gateway (Stripe) using token: {STRIPE_SECRET_KEY}")
    return {"status": "success", "amount": amount, "gateway": "Stripe"}

# =====================================================================
# 3. WEB APP COMPONENT (FRONTEND)
# =====================================================================
@app.route('/')
def web_app_home():
    """Giao diện Web App Frontend trả về HTML"""
    html_content = """
    <html>
        <head><title>Secure E-commerce Web App</title></head>
        <body style="font-family: Arial;">
            <h2>Welcome to E-commerce Portal</h2>
            <p>Hệ thống bao gồm: Web App, RESTful API, SQLite Database và External Payment (Stripe).</p>
        </body>
    </html>
    """
    return render_template_string(html_content)

# =====================================================================
# 4. API SERVER COMPONENT (BACKEND ENDPOINTS)
# =====================================================================

@app.route('/api/v1/auth/login', methods=['POST'])
def api_login():
    """API Xác thực kết nối thẳng vào Database"""
    username = request.form.get('username')
    password = request.form.get('password', '')

    # [LỖI MEDIUM 1: Weak Cryptography] - Semgrep cảnh báo dùng MD5
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    # Truy vấn vào Database thực tế
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "token": "jwt-mock-token"}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.route('/api/v1/invoices/download', methods=['GET'])
def api_download_invoice():
    """API Tải hóa đơn"""
    file_name = request.args.get("file_name")
    
    # [LỖI HIGH 2: Path Traversal] - SonarCloud & Semgrep báo lỗi
    base_dir = "/var/www/app/data/invoices/"
    target_path = os.path.join(base_dir, file_name)
    
    if os.path.exists(target_path):
        return send_file(target_path)
    return jsonify({"error": "Invoice not found"}), 404


@app.route('/api/v1/payment/checkout', methods=['GET'])
def api_payment_checkout():
    """API Thanh toán và Chẩn đoán mạng cổng thanh toán"""
    
    # [LỖI CRITICAL 1: OS Command Injection] - Cho phép tấn công chiếm quyền máy chủ
    target_ip = request.args.get("gateway_ip", "api.stripe.com")
    command = f"ping -c 1 {target_ip}"
    
    try:
        # Thực thi lệnh hệ thống từ input người dùng
        output = subprocess.check_output(command, shell=True, text=True)
        
        # Gọi sang External Payment Service
        payment_result = process_external_payment(100)
        
        return jsonify({"network_log": output, "payment_status": payment_result}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Gateway timeout"}), 500

# =====================================================================
# APPLICATION ENTRY POINT
# =====================================================================
if __name__ == '__main__':
    init_db()
    # [LỖI MEDIUM 2: Debug Mode Enabled] - Lộ thông tin nhạy cảm khi có lỗi
    app.run(host='0.0.0.0', port=8080, debug=True)