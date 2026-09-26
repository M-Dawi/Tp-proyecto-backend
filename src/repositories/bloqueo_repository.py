from db.db import get_db_connection

def obtener_bloqueo_por_id(bloqueo_id):
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bloqueos WHERE id = %s", (bloqueo_id,))
        bloqueo = cursor.fetchone()
        cursor.close()
        conexion.close()
        return bloqueo
    except Exception as e:
        print(f"Error de conexión al buscar bloqueo {bloqueo_id}: {e}")
        if conexion is not None:
            conexion.close()
        return None