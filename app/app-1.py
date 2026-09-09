# Lộ Secret / API Key
aws_access_key = "AKIAIOSFODNN7EXAMPLE"

# SQL Injection sơ đẳng
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    cursor.execute(query)