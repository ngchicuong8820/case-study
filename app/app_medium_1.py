from flask import Flask

app = Flask(__name__)

@app.route("/info")
def system_info():
    return "System is running smoothly."

if __name__ == "__main__":
    # Lỗ hổng Medium 1: Kích hoạt chế độ Debug trên môi trường mạng công cộng
    app.run(host="0.0.0.0", port=5000, debug=True)