import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route("/network-test")
def ping_test():
    target_ip = request.args.get("ip", "8.8.8.8")
    # Lỗ hổng Critical: Thực thi lệnh OS trực tiếp từ tham số request
    command = f"ping -c 1 {target_ip}"
    output = subprocess.check_output(command, shell=True, text=True)
    
    return f"<pre>{output}</pre>"