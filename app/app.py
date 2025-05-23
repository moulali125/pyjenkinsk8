from flask import Flask, request, jsonify
import mysql.connector
import time
 
app = Flask(__name__)
 
def get_connection():
    while True:
        try:
            connection = mysql.connector.connect(
                host="mysql_db",        # Docker Compose service name
                user="root",
                password="Relational@123",
                database="user_1",
                port=3306
            )
            return connection
        except:
            print("Waiting for DB...")
            time.sleep(2)
 
@app.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data['name']
    age = data['age']
   
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT
        )
    """)
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cursor.close()
    conn.close()
 
    return jsonify({"message": "User added successfully!"})
 
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, age FROM users")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


