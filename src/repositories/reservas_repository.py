from db.db import get_db_connection

def obtener_reserva_por_id(reserva_id):
    conexion = None
    try:
        # Selecciona las reservas que haya en la base de datos
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        query = "SELECT * FROM reservas WHERE id = %s"
        cursor.execute(query, (reserva_id,))
        reserva = cursor.fetchone()

        cursor.close()
        conexion.close()
        return reserva
    except Exception as e:
        print(f"Error de conexión al buscar reserva {reserva_id}: {e}")
        if conexion is not None:
            conexion.close()
        return None

def crear_reserva(datos):
    # Crea una reserva en la base de datos
    conexion = get_db_connection()
    cursor = conexion.cursor()
    
    query = """
        INSERT INTO reservas (id_cancha, id_socio, fecha_hora_inicio, fecha_hora_fin, precio_hora, precio_total, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    # OJO: precio_hora y precio_total todavía se esperan en 'datos' porque
    # el cálculo automático del servidor no está hecho todavía (pendiente)
    valores = (
        datos['id_cancha'],
        datos['id_socio'],
        datos['fecha_hora_inicio'],
        datos['fecha_hora_fin'],
        datos['precio_hora'],
        datos['precio_total'],
        datos.get('estado', 'confirmada')
    )
    cursor.execute(query, valores)
    conexion.commit()
    
    nuevo_id = cursor.lastrowid
    
    cursor.close()
    conexion.close()
    return nuevo_id

def actualizar_estado(id_reserva, nuevo_estado):
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("UPDATE reservas SET estado = %s WHERE id = %s", (nuevo_estado, id_reserva))
        conexion.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error de conexión al actualizar estado: {e}")
        return False
    finally:
        if conexion:
            conexion.close()
