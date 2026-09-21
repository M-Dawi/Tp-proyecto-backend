from src.repositories.socios_repository import (
    obtener_socios, obtener_socio_por_id, 
    obtener_socio_por_email, crear_socio, actualizar_socio
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
        
        socio_actualizado = obtener_socio_por_id(socio_id)
        socio_actualizado["activo"] = bool(socio_actualizado["activo"])

        return socio_actualizado, 200

    except Exception as e:

        print("Error:", e)

        return armar_error(
            "INTERNAL_SERVER_ERROR", 
            "Error interno del servidor", 
            "Ocurrió un error inesperado",
            500
        )
