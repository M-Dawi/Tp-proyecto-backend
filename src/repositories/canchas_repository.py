from db.db import get_db_connection

def obtener_canchas(
        id_deporte=None,
        nombre=None,
        techada=None,
        activa=None,
        limit=10,
        offset=0
):
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM canchas WHERE 1=1"
    params = []

    if id_deporte is not None:
        query += " AND id_deporte = %s"
        params.append(id_deporte)

    if nombre is not None:
        query += " AND nombre ILIKE %s"
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
    