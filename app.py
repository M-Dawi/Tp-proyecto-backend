from flask import Flask, jsonify
from repositories.db import get_db_connection

app = Flask(__name__)


@app.route('/api/deportes', methods=['GET'])
def obtener_deportes():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre FROM deportes;")
        deportes = cursor.fetchall()
        
        return jsonify(deportes), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
