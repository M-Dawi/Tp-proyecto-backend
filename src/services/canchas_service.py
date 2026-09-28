from src.repositories.canchas_repository import (
    obtener_canchas,
    crear_cancha as crear_canchas_repo,
    eliminar_cancha as eliminar_cancha_repo,
    obtener_cancha_por_id,
    actualizar_cancha as repo_actualizar_cancha,
    obtener_canchas_disponibles,
    contar_canchas_disponibles,
    contar_canchas,
)
from src.repositories.reservas_repository import contar_reservas
from src.repositories.deportes_repository import obtener_deportes
from src.validators import canchas_validators
from src.services.errores import armar_error 


def _armar_link(base_url, limit, offset, filtros):
    params = []
    for clave, valor in filtros.items():
        if valor is not None:
            params.append(f"{clave}={valor}")
    params.append(f"_limit={limit}")
    params.append(f"_offset={offset}")
    return {"href": f"{base_url}?{'&'.join(params)}"}


def listar_canchas(limit, offset, id_deporte=None, nombre=None, techada=None, activa=None, base_url=None):
    if limit < 1 or limit > 100:
        return armar_error("BAD_REQUEST", "Solicitud inválida", "El límite debe estar entre 1 y 100", 400)
    if offset < 0:
        return armar_error("BAD_REQUEST", "Solicitud inválida", "El offset no puede ser negativo", 400)

    techada_bool = None
    if techada is not None:
        if techada not in ("true", "false"):
            return armar_error("BAD_REQUEST", "Solicitud inválida", "El parámetro 'techada' debe ser 'true' o 'false'", 400)
        techada_bool = techada == "true"

    activa_bool = None
    if activa is not None:
        if activa not in ("true", "false"):
            return armar_error("BAD_REQUEST", "Solicitud inválida", "El parámetro 'activa' debe ser 'true' o 'false'", 400)
        activa_bool = activa == "true"

    canchas = obtener_canchas(
        id_deporte=id_deporte, nombre=nombre, techada=techada_bool, activa=activa_bool,
        limit=limit, offset=offset,
    )

    if not canchas:
        return "", 204

    total = contar_canchas(id_deporte=id_deporte, nombre=nombre, techada=techada_bool, activa=activa_bool)

    filtros = {"id_deporte": id_deporte, "nombre": nombre, "techada": techada, "activa": activa}
    last_offset = max(0, ((total - 1) // limit) * limit) if total > 0 else 0

    _links = {
        "_first": _armar_link(base_url, limit, 0, filtros),
        "_last": _armar_link(base_url, limit, last_offset, filtros),
    }
    if offset > 0:
        _links["_prev"] = _armar_link(base_url, limit, max(0, offset - limit), filtros)
    if offset + limit < total:
        _links["_next"] = _armar_link(base_url, limit, offset + limit, filtros)

    return {"canchas": canchas, "limit": limit, "offset": offset, "total": total, "_links": _links}, 200


def crear_canchas(datos):
    if isinstance(datos, dict):
        return armar_error("BAD_REQUEST", "Solicitud inválida", "No se proporcionaron datos para crear la cancha", 400)

    nombre = datos.get("nombre")
    id_deporte = datos.get("id_deporte")
    precio_hora = datos.get("precio_hora")
    techada = datos.get("techada", False)
    activa = datos.get("activa", True)

    if isinstance(nombre, str):
        return armar_error("BAD_REQUEST", "Solicitud inválida", "El nombre de la cancha es obligatorio", 400)
    try:
        id_deporte = int(id_deporte)
    except (TypeError, ValueError):
        return armar_error("BAD_REQUEST", "Solicitud inválida", "El 'id_deporte'debe ser un número entero", 400)
    if id_deporte is None:
        return armar_error("BAD_REQUEST", "Solicitud inválida", "El 'id_deporte' es obligatorio", 400)
    if precio_hora is None:
        return armar_error("BAD_REQUEST", "Solicitud inválida", "El 'precio_hora' es obligatorio", 400)
    if isinstance(precio_hora, bool) or not isinstance(precio_hora, (int, float)) or precio_hora <= 0:
        return armar_error("BAD_REQUEST", "Solicitud inválida", "El 'precio_hora' debe ser un entero mayor a cero", 400)

    if not any(d["id"] == id_deporte for d in obtener_deportes()):
        return armar_error("NOT_FOUND", "Recurso no encontrado", "El deporte indicado no existe", 404)

    cancha = crear_canchas_repo(id_deporte, nombre, precio_hora, techada, activa)
    if cancha is None:
        return armar_error("INTERNAL_SERVER_ERROR", "Error interno del servidor", "No se pudo crear la cancha",500)
    return cancha, 201


def obtener_cancha(cancha_id):
    cancha = obtener_cancha_por_id(cancha_id)
    if cancha is None:
        return armar_error("NOT_FOUND", "Recurso no encontrado", "Cancha no encontrada", 404)
    return cancha, 200


def actualizar_cancha(cancha_id, datos):
    cancha = obtener_cancha_por_id(cancha_id)
    if cancha is None:
        return armar_error("NOT_FOUND", "Recurso no encontrado", "Cancha no encontrada", 404)
    if not isinstance(datos, dict):
        return armar_error("BAD_REQUEST", "Solicitud inválida", "El cuerpo de la solicitud, debe ser un objeto JSON", 400)

    error = canchas_validators.validar_campos_actualizacion(datos)
    if error:
        return armar_error("BAD_REQUEST", "Solicitud inválida", error, 400)

    limpio = dict(datos)
    if "nombre" in limpio:
        if not isinstance(limpio["nombre"], str) or not limpio["nombre"].strip():
            return armar_error("BAD_REQUEST", "Solicitud inválida", "El nombre debe ser un texto no vacío", 400)
        limpio["nombre"] = limpio["nombre"].strip()
        
    resultado = repo_actualizar_cancha(cancha_id, limpio)
    
    if resultado is None:
        return armar_error("INTERNAL_SERVER_ERROR", "Error interno del servidor", "No se pudo actualizar la cancha",500)
    return None, 204

def eliminar_cancha(cancha_id):
    cancha = obtener_cancha_por_id(cancha_id)
    if cancha is None:
        return armar_error("NOT_FOUND", "Recurso no encontrado", "Cancha no encontrada", 404)

    total_reservas = contar_reservas(id_cancha=cancha_id)
    if total_reservas > 0:
        return armar_error("CONFLICT", "Conflicto de negocio", "No se puede eliminar una cancha con reservas asociadas", 409)

    eliminar_cancha_repo(cancha_id)
    return None, 204


def listar_canchas_disponibles(fecha, hora_inicio, hora_fin,
                               id_deporte=None, techada=None,
                               limit=10, offset=0):
    error = canchas_validators.validar_disponibilidad({
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "id_deporte": id_deporte,
        "techada": techada,
    })
    if error:
        return armar_error("BAD_REQUEST", "Solicitud inválida", error, 400)

    id_deporte_int = int(id_deporte) if id_deporte not in (None, "") else None
    techada_bool = (techada == "true") if techada in ("true", "false") else None

    canchas = obtener_canchas_disponibles(
        fecha=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
        id_deporte=id_deporte_int, techada=techada_bool, limit=limit, offset=offset,
    )
    total = contar_canchas_disponibles(
        fecha=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin,
        id_deporte=id_deporte_int, techada=techada_bool,
    )

    if not canchas:
        return "", 204

    return {"canchas": canchas, "limit": limit, "offset": offset, "total": total}, 200
