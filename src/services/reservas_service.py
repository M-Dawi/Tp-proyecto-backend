from datetime import datetime, timezone, timedelta
from src.repositories.reservas_repository import obtener_reserva_por_id, crear_reserva, actualizar_estado, listar_reservas, contar_reservas, buscar_solapamientos
from src.validators.reservas_validators import validar_campos_creacion, validar_estado
from src.validators.fechas import parsear_fecha_hora, validar_intervalo_reserva, formatear_fecha_hora
from src.repositories.canchas_repository import obtener_cancha_por_id
from src.repositories.socios_repository import obtener_socio_por_id

def consultar_reserva_por_id(reserva_id):
    reserva = obtener_reserva_por_id(reserva_id)
    if not reserva:
        return None

    reserva['fecha_hora_inicio'] = reserva['fecha_hora_inicio'].strftime("%Y-%m-%dT%H:%M:%S.%f") + "-03:00"
    reserva['fecha_hora_fin'] = reserva['fecha_hora_fin'].strftime("%Y-%m-%dT%H:%M:%S.%f") + "-03:00"
    reserva['precio_hora'] = int(reserva['precio_hora'])
    reserva['precio_total'] = int(reserva['precio_total'])
    reserva['created_at'] = str(reserva['created_at'])

    return reserva

def validar_datos_reserva(datos):
    error_campos = validar_campos_creacion(datos)
    if error_campos is not None:
        return ({"error": error_campos}, 400), None 
    id_cancha = datos['id_cancha']
    id_socio = datos['id_socio']
    inicio = parsear_fecha_hora(datos['fecha_hora_inicio'])
    fin = parsear_fecha_hora(datos['fecha_hora_fin'])
    if inicio is None or fin is None: 
        return ({"error": "La fecha tiene formato invalido"}, 400)
    intervalo = validar_intervalo_reserva(inicio, fin)
    if intervalo is not None:
        return ({"error": intervalo}, 400), None
    cancha = obtener_cancha_por_id(id_cancha)
    if cancha is None: 
        return ({"error": "La cancha no existe"}, 404), None
    if not cancha['activa']:
        return ({"error": "La cancha no esta activa"}, 409), None
    socio = obtener_socio_por_id(id_socio)
    if socio is None:
        return ({"error": "El socio no existe"}, 404), None
    if not socio['activo']: 
        return ({"error": "El socio no esta activo"}, 409), None
    solapamiento_cancha = buscar_solapamientos("id_cancha", id_cancha, inicio, fin)
    solapamiento_socio = buscar_solapamientos("id_socio", id_socio, inicio, fin)
    if solapamiento_cancha is not None or solapamiento_socio is not None:
        return ({"error": "Se superpone el horario"}, 409), None
    return None, {"inicio": inicio, "fin": fin, "cancha": cancha}


def registrar_reserva(datos):
    error, datos_validados = validar_datos_reserva(datos)
    if error is not None:
        return error
    inicio = datos_validados['inicio']
    fin = datos_validados['fin']
    precio_hora = datos_validados['cancha']['precio_hora']
    horas = ((fin - inicio).total_seconds())/3600
    precio_total = int(precio_hora * horas)  
    nuevo_id = crear_reserva(datos, precio_hora, precio_total)
    nueva_reserva = consultar_reserva_por_id(nuevo_id)
    return nueva_reserva, 201

TRANSICIONES_PERMITIDAS = {
    "confirmada": {
        "cancelada": lambda ahora, inicio, fin: ahora < inicio,
        "finalizada": lambda ahora, inicio, fin: ahora >= fin,
    },
}

zona_horaria = timezone(timedelta(hours=-3))

def cambiar_estado(reserva_id, nuevo_estado):
    error_estado = validar_estado(nuevo_estado)
    if error_estado is not None:
        return {"error": error_estado}, 400

    reserva = obtener_reserva_por_id(reserva_id)
    if reserva is None:
        return {"error": "La reserva no existe"}, 404

    if nuevo_estado == reserva["estado"]:
        return None, 204

    transiciones_desde_actual = TRANSICIONES_PERMITIDAS.get(reserva["estado"])
    if transiciones_desde_actual is None:
        return {"error": f"No se puede modificar una reserva en estado '{reserva['estado']}'"}, 409

    condicion = transiciones_desde_actual.get(nuevo_estado)
    if condicion is None:
        return {"error": f"No se puede pasar de '{reserva['estado']}' a '{nuevo_estado}'"}, 409

    ahora = datetime.now(zona_horaria)
    if not condicion(ahora, reserva["fecha_hora_inicio"], reserva["fecha_hora_fin"]):
        return {"error": f"No se puede pasar a '{nuevo_estado}' en este momento"}, 409

    actualizado = actualizar_estado(reserva_id, nuevo_estado)
    if not actualizado:
        return {"error": "No se pudo actualizar la reserva"}, 500

    return None, 204
    #-------

def armar_url_hateoas(base_url, limit, offset, filtros):
    params = []
    for clave, valor in filtros.items():
        if valor is not None:
            params.append(f"{clave}={valor}")
            
    params.append(f"_limit={limit}")
    params.append(f"_offset={offset}")
    
    query_string = "&".join(params)
    return f"{base_url}?{query_string}"

def listar_reservas_service(id_cancha, id_socio, estado, fecha_desde, fecha_hasta, limit, offset, base_url):
    # obtener la lista y el conteo de BD
    reservas_db = listar_reservas(id_cancha, id_socio, estado, fecha_desde, fecha_hasta, limit, offset)
    total_registros = contar_reservas(id_cancha, id_socio, estado, fecha_desde, fecha_hasta)

    items = []
    for r in reservas_db:
        items.append({
            "id": int(r["id"]),
            "id_socio": int(r["id_socio"]),
            "id_cancha": int(r["id_cancha"]),
            "fecha_hora_inicio": formatear_fecha_hora(r["fecha_hora_inicio"]) if r.get("fecha_hora_inicio") else None,
            "fecha_hora_fin": formatear_fecha_hora(r["fecha_hora_fin"]) if r.get("fecha_hora_fin") else None,
            "estado": str(r["estado"]),
            "precio_hora": int(r["precio_hora"]),
            "precio_total": int(r["precio_total"]),
            "created_at": formatear_fecha_hora(r["created_at"]) if r.get("created_at") else None
        })

    # genera los links HATEOAS (_links)
    filtros = {
        "id_cancha": id_cancha,
        "id_socio": id_socio,
        "estado": estado,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    }

    links = {
        "first": armar_url_hateoas(base_url, limit, 0, filtros),
        "last": armar_url_hateoas(base_url, limit, max(0, ((total_registros - 1) // limit) * limit), filtros)
    }

    if offset > 0:
        prev_offset = max(0, offset - limit)
        links["prev"] = armar_url_hateoas(base_url, limit, prev_offset, filtros)

    if offset + limit < total_registros:
        next_offset = offset + limit
        links["next"] = armar_url_hateoas(base_url, limit, next_offset, filtros)

    respuesta = {
        "items": items,
        "_links": links
    }

    return respuesta, 200