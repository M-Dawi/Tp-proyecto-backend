from db.db import get_db_connection

def obtener_reserva_por_id(reserva_id):
    # Selecciona las reservas que haya en la base de datos
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)
    
    query = "SELECT * FROM reservas WHERE id = %s"
    cursor.execute(query, (reserva_id,))
    reserva = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    return reserva
