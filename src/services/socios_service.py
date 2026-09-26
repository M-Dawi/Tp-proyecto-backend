from src.repositories.socios_repository import (
    obtener_socios, obtener_socio_por_id, 
    obtener_socio_por_email, crear_socio, actualizar_socio, contar_socios
)

from src.validators.socios_validator import validar_datos_crear_socio, validar_datos_actualizar_socio

def armar_error(code, message, description, status_code):
    return {
        "errors": [
            {
                "code": code,
                "message": message,
                "level": "error",
                "description": description
            }
        ]
    }, status_code

LIMIT_DEFAULT = 10
LIMIT_MAX = 100
OFFSET_DEFAULT = 0

def leer_paginacion(args):
    try:
        limit = int(args.get("_limit", LIMIT_DEFAULT))
        offset = int(args.get("_offset", OFFSET_DEFAULT))
    except (TypeError, ValueError):
        return None
    if not (1 <= limit <= LIMIT_MAX) or offset < 0:
        return None
    return limit, offset

def crear_socio_service(cuerpo):

    error_validacion = validar_datos_crear_socio(cuerpo)  # Función desde validators

    if error_validacion:
        return armar_error("BAD_REQUEST", "Solicitud inválida", error_validacion, 400)

    nombre = cuerpo.get("nombre")
    email = cuerpo.get("email")

    nombre_limpio = nombre.strip()
    email_limpio = email.strip().lower()

    try:

        socio_existente_por_email = obtener_socio_por_email(email_limpio)  # Funcion desde repository

        if socio_existente_por_email:
            return armar_error(
                "CONFLICT",
                "Conflicto de negocio",
                "El email ya se encuentra registrado por otro socio.",
                409
            )

        nuevo_id = crear_socio(nombre_limpio, email_limpio)  # Funciones desde repository
        nuevo_socio = obtener_socio_por_id(nuevo_id)

        nuevo_socio["activo"] = bool(nuevo_socio["activo"])

        return nuevo_socio, 201

    except Exception as e:

        print("Error:", e)

        return armar_error(
            "INTERNAL_SERVER_ERROR", 
            "Error interno del servidor", 
            "Ocurrió un error inesperado",
            500
        )

def actualizar_socio_service(socio_id, cuerpo):
    error_validacion = validar_datos_actualizar_socio(cuerpo)  # Función desde validators

    if error_validacion:
        return armar_error("BAD_REQUEST", "Solicitud inválida", error_validacion, 400)

    try:

        socio_encontrado = obtener_socio_por_id(socio_id)  # Funcion desde repository

        if socio_encontrado is None:
            return armar_error("NOT_FOUND", "Recurso no encontrado", "No se encuentra socio en nuestra base de datos", 404)
    
        datos = {}

        if "nombre" in cuerpo:
            nombre = cuerpo.get("nombre")
            datos["nombre"] = nombre.strip()

        if "email" in cuerpo:
            email = cuerpo.get("email")
            datos["email"] = email.strip().lower()

        if "activo" in cuerpo:
            activo = cuerpo.get("activo")
            datos["activo"] = activo

        if "email" in datos:
            socio_por_email = obtener_socio_por_email(datos["email"])  # Funcion desde repository
            if socio_por_email is not None and socio_id != socio_por_email["id"]:
                return armar_error(
                    "CONFLICT",
                    "Conflicto de negocio",
                    "El email ya se encuentra registrado por otro socio.",
                    409
                )

        actualizar_socio(socio_id,datos)

        return None, 204

    except Exception as e:

        print("Error:", e)

        return armar_error(
            "INTERNAL_SERVER_ERROR", 
            "Error interno del servidor", 
            "Ocurrió un error inesperado",
            500
        )

def obtener_socios_service(limit, offset, nombre, activo):

    if activo is not None:
        if activo.lower() not in ["true", "false"]:          #si el parámetro activo no es true o false, devuelve un error 400
            return armar_error(
                "BAD_REQUEST",
                "Solicitud inválida",
                "El parámetro 'activo' debe ser 'true' o 'false'",
                400
            )
        activo = activo.lower() == "true"  # Convertir a booleano
    

    try:

        socios = obtener_socios(limit, offset, nombre, activo)  # Función desde repository
        if not socios:                            #si no encuntra socios, devuelve un error 204
            return "", 204
                
        total = contar_socios(nombre, activo)  # Función desde repository
        

        prev_offset = max(0, offset - limit)
        next_offset = offset + limit 
        last_offset = ((total - 1) // limit) * limit 

        respuesta = {
            "socios": socios,
            "_links": {
                "_first": {
                    "href": f"http://localhost:5000/socios?_offset=0&_limit={limit}",
                },
                "_prev": {
                    "href": f"http://localhost:5000/socios?_offset={prev_offset}&_limit={limit}",
                
                },
                "_next": {
                    "href": f"http://localhost:5000/socios?_offset={next_offset}&_limit={limit}",
                },
                "_last": {
                    "href": f"http://localhost:5000/socios?_offset={last_offset}&_limit={limit}",
                }

            }
        }


       
        return respuesta, 200                        #si encuentra socios, devuelve la lista de socios y un código 200
    
    except Exception as e:
        print("Error:", e)
        return armar_error(
            "INTERNAL_SERVER_ERROR",
            "Error interno del servidor",
            "Ocurrió un error inesperado",
            500
        )


def obtener_socio_por_id_service(socio_id):
    try:
        socio = obtener_socio_por_id(socio_id)  # Función desde repository
        if socio is None:                       #si no se encuentra el socio, devuelve un error 404
            return armar_error(            
                        "NOT_FOUND", 
                        "Recurso no encontrado",    
                        "No se encuentra socio en nuestra base de datos", 
                        404
                        )
        return socio, 200                       #si se encuentra el socio, devuelve el socio y un código 200
    except Exception as e:                      #si ocurre un error inesperado(conexion), devuelve un error 500
        print("Error:", e)
        return armar_error(
            "INTERNAL_SERVER_ERROR", 
            "Error interno del servidor", 
            "Ocurrió un error inesperado",
            500
        )
  

