from db.db import get_db_connection

def obtener_socios(limit=10, offset=0, nombre=None, activo=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM socios"
    cursor.execute(query)
    socios = cursor.fetchall()
    cursor.close()
    conn.close()
    return socios

def obtener_socio_por_id(socio_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM socios where id = %s"
    cursor.execute(query, (socio_id,))
    socio = cursor.fetchone()
    cursor.close()
    conn.close()
    return socio

def obtener_socio_por_email(email_socio):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM socios where email = %s"
    cursor.execute(query, (email_socio,))
    socio = cursor.fetchone()

    cursor.close()
    conn.close()
    return socio

def crear_socio(nombre, email):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO socios(nombre, email) VALUES (%s, %s)"
    cursor.execute(query, (nombre, email))
    conn.commit()
    id_nuevo = cursor.lastrowid

    cursor.close()
    conn.close()
    return id_nuevo

def actualizar_socio(socio_id, datos):
    conn = get_db_connection()
    cursor = conn.cursor()

    campos = []
    valores = []

    if 'nombre' in datos:
        campos.append("nombre = %s")
        valores.append(datos['nombre'])
    if 'activo' in datos:
        campos.append("activo = %s")
        valores.append(datos['activo']) 
    if 'email' in datos:
        campos.append("email = %s")
        valores.append(datos['email'])

    query = "UPDATE socios SET " + ", ".join(campos) + " WHERE id = %s"
    valores.append(socio_id)
    
    cursor.execute(query, tuple(valores))
    conn.commit()
    cursor.close()
    conn.close()