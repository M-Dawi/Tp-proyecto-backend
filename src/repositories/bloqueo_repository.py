from db.db import get_db_connection


def cancha_existe(conn, cancha_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM canchas WHERE id = %s", (cancha_id,))
    result = cursor.fetchone() is not None
    cursor.close()
    return result 

def crear_bloqueo(conn, cancha_id, fecha_inicio, fecha_fin):
    cursor = conn.cursor()
    
    if reserva:
        cursor.close()
        return {'tipo': 'reserva', 'id': reserva['id']}
        cursor.excute("SELECT id FROM reservas WHERE cancha_id = %s AND fecha_inicio < %s AND fecha_fin > %s", (cancha_id, fecha_fin, fecha_inicio))
    bloqueo = cursor.fetchone()
    cursor.close()
    return {'tipo': 'bloqueo', 'id': bloqueo['id']} if bloqueo else None

def insertar_bloqueo(conn, cancha_id, fecha_inicio, fecha_fin):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bloqueos (cancha_id, fecha_inicio, fecha_fin) VALUES (%s, %s, %s)",
        (cancha_id, fecha_inicio, fecha_fin)
    )
    conn.commit()
    bloqueo_id = cursor.lastrowid
    cursor.close()
    return bloqueo_id

    

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

def eliminar_bloqueo(bloqueo_id):
    conexion = None
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM bloqueos WHERE id = %s", (bloqueo_id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error de conexión al eliminar bloqueo {bloqueo_id}: {e}")
        if conexion is not None:
            conexion.close()
        return False

def contar_bloqueos(id_cancha=None, fecha=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    filtros = []
    valores = []

    if id_cancha is not None:
        filtros.append("id_cancha = %s")
        valores.append(id_cancha)
    if fecha is not None:
        filtros.append("fecha = %s")
        valores.append(fecha)

    query = "SELECT COUNT(*) FROM bloqueos"
    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    cursor.execute(query, tuple(valores))
    total_bloqueos = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return total_bloqueos

def listar_bloqueos(id_cancha=None, fecha=None, limit=10, offset=0):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    filtros = []
    valores = []

    if id_cancha is not None:
        filtros.append("id_cancha = %s")
        valores.append(id_cancha)
    if fecha is not None:
        filtros.append("fecha = %s")
        valores.append(fecha)

    query = "SELECT * FROM bloqueos"

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    query += " ORDER BY id ASC LIMIT %s OFFSET %s"

    valores.append(limit)
    valores.append(offset)

    cursor.execute(query, tuple(valores))
    bloqueos = cursor.fetchall()
    cursor.close()
    conn.close()
    return bloqueos   
