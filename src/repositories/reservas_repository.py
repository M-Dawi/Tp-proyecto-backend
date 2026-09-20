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

def crear_reserva(datos):
    # Crea una reserva en la base de datos
    conexion = get_db_connection()
    cursor = conexion.cursor()
    
    query = """
        INSERT INTO reservas (id_cancha, id_socio, fecha, hora_inicio, hora_fin, monto_total, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        datos['id_cancha'],
        datos['id_socio'],
        datos['fecha'],
        datos['hora_inicio'],
        datos['hora_fin'],
        datos['monto_total'],
        datos.get('estado', 'confirmada')
    )
    
    cursor.execute(query, valores)
    conexion.commit()
    
    nuevo_id = cursor.lastrowid
    
    cursor.close()
    conexion.close()
    return nuevo_id
