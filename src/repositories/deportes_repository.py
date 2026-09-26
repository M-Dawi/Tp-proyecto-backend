from db.db import get_db_connection

def obtener_deportes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT id, nombre FROM deportes"
    cursor.execute(query)
    deportes = cursor.fetchall()
    cursor.close()
    conn.close()
    return deportes
