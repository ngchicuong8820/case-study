from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/exec")
def execute_command():
    # Lỗi Critical: Thực thi lệnh hệ thống trực tiếp từ tham số người dùng (Command Injection)
    cmd = request.args.get("cmd", "")
    output = os.popen(cmd).read()
    return f"Execution result: {output}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)