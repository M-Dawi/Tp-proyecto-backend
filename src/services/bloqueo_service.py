from src.repositories.bloqueo_repository import (
    obtener_bloqueo_por_id,
    eliminar_bloqueo,
    contar_bloqueos,
    listar_bloqueos,
    crear_bloqueo,
)
from src.repositories.canchas_repository import obtener_cancha_por_id
from src.services.errores import armar_error

def eliminar_bloqueo_service(bloqueo_id):
    try:
        bloqueo = obtener_bloqueo_por_id(bloqueo_id)
        if bloqueo is None:
            return armar_error(            
                    "NOT_FOUND", 
                    "Recurso no encontrado",    
                    "No se encuentra bloqueo en nuestra base de datos", 
                    404
                    )
        esta_bloqueado = eliminar_bloqueo(bloqueo_id)
        if esta_bloqueado:
            return None, 204
        else:
            return armar_error(
                "INTERNAL_SERVER_ERROR", 
                "Error interno del servidor", 
                "Error de conexión al eliminar bloqueo",
                500
            )
    except Exception as e:
        print("Error:", e)
        return armar_error(
            "INTERNAL_SERVER_ERROR", 
            "Error interno del servidor", 
            "Ocurrió un error inesperado",
            500
        )

# GET/service/bloqueo_service---
def obtener_bloqueos_service(filtros, base_url):
    id_cancha = filtros["id_cancha"]
    fecha = filtros["fecha"]
    limit = filtros["limit"]
    offset = filtros["offset"]

    try:
     filas = listar_bloqueos(id_cancha, fecha, limit, offset)

     if not filas:
         return "", 204

     total = contar_bloqueos(id_cancha, fecha)

     bloqueos = []
     for fila in filas:
        bloqueos.append({
            "id": int(fila["id"]),
            "id_cancha": int(fila["id_cancha"]),
            "fecha": str(fila["fecha"]),
            "hora_inicio": str(fila["hora_inicio"])[:8],
            "hora_fin": str(fila["hora_fin"])[:8],
            "motivo": str(fila["motivo"]) if fila.get("motivo") else ""
        })

     return {
        "bloqueos": bloqueos,
        "_links": _armar_links(base_url, id_cancha, fecha, limit, offset, total)
     }, 200

    except Exception as e:
        print("Error:", e)
        return armar_error(
                    "INTERNAL_SERVER_ERROR", 
                    "Error interno del servidor", 
                    "Ocurrió un error inesperado",
                    500
                )


def _armar_links(base_url, id_cancha, fecha, limit, offset, total):
    def construir(nuevo_offset):
        params = []
        if id_cancha is not None:
            params.append(f"id_cancha={id_cancha}")
        if fecha is not None:
            params.append(f"fecha={fecha}")
        params.append(f"_offset={nuevo_offset}")
        params.append(f"_limit={limit}")
        return {"href": f"{base_url}?{'&'.join(params)}"}

    ultimo_offset = 0 if total == 0 else ((total - 1) // limit) * limit

    links = {
        "_first": construir(0),
        "_last": construir(ultimo_offset)
    }

    if offset > 0:
        links["_prev"] = construir(max(0, offset - limit))

    if offset + limit < total:
        links["_next"] = construir(offset + limit)

    return links

def crear_bloqueo_service(datos):
    cancha = obtener_cancha_por_id(datos["id_cancha"])
    if cancha is None:
        return armar_error("NOT_FOUND", "Recurso no encontrado", "La cancha no existe", 404)

    try:
        bloqueo = crear_bloqueo(
            datos["id_cancha"], datos["fecha"], datos["hora_inicio"], datos["hora_fin"], datos["motivo"],
        )

        if bloqueo is None:
            return armar_error("INTERNAL_SERVER_ERROR", "Error interno del servidor", "No se pudo crear el bloqueo", 500)

        return {
            "id": int(bloqueo["id"]),
            "id_cancha": int(bloqueo["id_cancha"]),
            "fecha": str(bloqueo["fecha"]),
            "hora_inicio": str(bloqueo["hora_inicio"])[:8],
            "hora_fin": str(bloqueo["hora_fin"])[:8],
            "motivo": str(bloqueo["motivo"]) if bloqueo.get("motivo") else ""
        }, 201

    except Exception as e:
        print("Error:", e)
        return armar_error("INTERNAL_SERVER_ERROR", "Error interno del servidor", "Ocurrió un error inesperado", 500)