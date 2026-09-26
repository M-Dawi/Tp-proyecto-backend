from db.db import get_db_connection # pyright: ignore[reportMissingImports]

def obtener_canchas(
        id_deporte=None,
        nombre=None,
        techada=None,
        activa=None,
        limit=10,
        offset=0
):
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM canchas WHERE 1=1"
    params = []

    if id_deporte is not None:
        query += " AND id_deporte = %s"
        params.append(id_deporte)

    if nombre is not None:
        query += " AND nombre LIKE %s"
        params.append(f"%{nombre}%")

    if techada is not None:
        query += " AND techada = %s"
        params.append(techada)

    if activa is not None:
        query += " AND activa = %s"
        params.append(activa)

    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cursor.execute(query, tuple(params))
    canchas = cursor.fetchall()

    cursor.close()
    conn.close()

    return canchas


def obtener_cancha_por_id(cancha_id):
    conexion = None
    try:
        # Selecciona las canchas que haya en la base de datos
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        query = "SELECT * FROM canchas WHERE id = %s"
        cursor.execute(query, (cancha_id,))
        cancha = cursor.fetchone()

        cursor.close()
        conexion.close()
        return cancha
    except Exception as e:
        print(f"Error de conexión al buscar la cancha {cancha_id}: {e}")
        if conexion is not None:
            conexion.close()
        return None



def crear_cancha(id_deporte, nombre, techada, activa):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO canchas (id_deporte, nombre, techada, activa)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (id_deporte, nombre, techada, activa))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "id_deporte": id_deporte,
        "nombre": nombre,
        "techada": techada,
        "activa": activa
    }


def actualizar_cancha(cancha_id, campos):
    if not campos:
        return obtener_cancha_por_id(cancha_id)

    permitidos = {"nombre", "precio_hora", "techada", "activa"}
    campos = {k: v for k, v in campos.items() if k in permitidos}

    if not campos:
        return obtener_cancha_por_id(cancha_id)

    sets = ", ".join(f"{col} = %s" for col in campos.keys())
    valores = list(campos.values()) + [cancha_id]

    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"UPDATE canchas SET {sets} WHERE id = %s"
    cursor.execute(query, tuple(valores))

    conn.commit()
    cursor.close()
    conn.close()

    return obtener_cancha_por_id(cancha_id)