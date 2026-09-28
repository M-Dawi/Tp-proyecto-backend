from db.db import get_db_connection
from datetime import datetime

def obtener_reserva_por_id(reserva_id):
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        query = "SELECT * FROM reservas WHERE id = %s"
        cursor.execute(query, (reserva_id,))
        reserva = cursor.fetchone()

        cursor.close()
        conexion.close()

        if reserva:
            if 'precio_hora' in reserva and reserva['precio_hora'] is not None:
                reserva['precio_hora'] = float(reserva['precio_hora'])
            if 'precio_total' in reserva and reserva['precio_total'] is not None:
                reserva['precio_total'] = float(reserva['precio_total'])

        return reserva
    except Exception as e:
        print(f"Error de conexión al buscar reserva {reserva_id}: {e}")
        if conexion is not None:
            conexion.close()
        return None

def buscar_solapamientos(columna, id_col, inicio, fin):
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        inicio_str = inicio.strftime("%Y-%m-%d %H:%M:%S")
        fin_str = fin.strftime("%Y-%m-%d %H:%M:%S")

        query = f"""
        SELECT * FROM reservas  
        WHERE {columna} = %s
            AND estado = 'confirmada'
            AND fecha_hora_inicio < %s
            AND fecha_hora_fin > %s
        """
        cursor.execute(query, (id_col, fin_str, inicio_str))
        solapamiento = cursor.fetchone()

        cursor.close()
        conexion.close()
        return solapamiento
    except Exception as e:
        print(f"error: {e}")
        if conexion is not None:
            conexion.close()
        return None 

def crear_reserva(datos, precio_hora, precio_total):
    conexion = get_db_connection()
    cursor = conexion.cursor()

    query = """
        INSERT INTO reservas (id_cancha, id_socio, fecha_hora_inicio, fecha_hora_fin, precio_hora, precio_total, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        datos['id_cancha'],
        datos['id_socio'],
        datos['fecha_hora_inicio'],
        datos['fecha_hora_fin'],
        precio_hora,
        precio_total,
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
    
 #LISTAR RESERVAS : funciones  que se comunicaran con la BD----

def listar_reservas(id_cancha=None, id_socio=None, estado=None, fecha_desde=None, fecha_hasta=None, limit=10, offset=0):
   
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)
    
    query_base = "SELECT id, id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total, created_at FROM reservas"
    condiciones = []
    valores = []

    if id_cancha is not None:
        condiciones.append("id_cancha = %s")
        valores.append(id_cancha)
        
    if id_socio is not None:
        condiciones.append("id_socio = %s")
        valores.append(id_socio)
        
    if estado is not None:
        condiciones.append("estado = %s")
        valores.append(estado)
        
    if fecha_desde is not None:
        condiciones.append("DATE(fecha_hora_inicio) >= %s")
        valores.append(fecha_desde)
        
    if fecha_hasta is not None:
        condiciones.append("DATE(fecha_hora_inicio) <= %s")
        valores.append(fecha_hasta)

    if condiciones:
        query_base += " WHERE " + " AND ".join(condiciones)

    query_base += " ORDER BY id ASC LIMIT %s OFFSET %s"
    valores.extend([limit, offset])

    cursor.execute(query_base, valores)
    reservas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return reservas


def contar_reservas(id_cancha=None, id_socio=None, estado=None, fecha_desde=None, fecha_hasta=None):
   
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)
    
    query_base = "SELECT COUNT(*) as total FROM reservas"
    condiciones = []
    valores = []

    if id_cancha is not None:
        condiciones.append("id_cancha = %s")
        valores.append(id_cancha)
        
    if id_socio is not None:
        condiciones.append("id_socio = %s")
        valores.append(id_socio)
        
    if estado is not None:
        condiciones.append("estado = %s")
        valores.append(estado)
        
    if fecha_desde is not None:
        condiciones.append("DATE(fecha_hora_inicio) >= %s")
        valores.append(fecha_desde)
        
    if fecha_hasta is not None:
        condiciones.append("DATE(fecha_hora_inicio) <= %s")
        valores.append(fecha_hasta)

    if condiciones:
        query_base += " WHERE " + " AND ".join(condiciones)

    cursor.execute(query_base, valores)
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado['total'] if resultado else 0