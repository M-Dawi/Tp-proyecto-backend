from datetime import datetime, timezone, timedelta

from src.repositories.reservas_repository import obtener_reserva_por_id, crear_reserva, actualizar_estado, listar_reservas, contar_reservas, buscar_solapamientos
from src.validators.reservas_validators import validar_campos_creacion, validar_estado

from src.validators.fechas import parsear_fecha_hora, validar_intervalo_reserva, formatear_fecha_hora

from src.repositories.canchas_repository import obtener_cancha_por_id

from src.repositories.socios_repository import obtener_socio_por_id

from src.services.errores import armar_error

def consultar_reserva_por_id(reserva_id):
    reserva = obtener_reserva_por_id(reserva_id)
    if not reserva:
        return None

    reserva['fecha_hora_inicio'] = reserva['fecha_hora_inicio'].strftime("%Y-%m-%dT%H:%M:%S.%f") + "-03:00"
    reserva['fecha_hora_fin'] = reserva['fecha_hora_fin'].strftime("%Y-%m-%dT%H:%M:%S.%f") + "-03:00"
    reserva['precio_hora'] = int(reserva['precio_hora'])
    reserva['precio_total'] = int(reserva['precio_total'])
    reserva.pop('created_at', None)

    return reserva

def validar_datos_reserva(datos):
    error_campos = validar_campos_creacion(datos)
    if error_campos is not None:
        return armar_error("BAD_REQUEST", "Solicitud inválida", error_campos, 400), None

    id_cancha = datos['id_cancha']
    id_socio = datos['id_socio']
    inicio = parsear_fecha_hora(datos['fecha_hora_inicio'])
    fin = parsear_fecha_hora(datos['fecha_hora_fin'])
    if inicio is None or fin is None:
        return armar_error("BAD_REQUEST", "Solicitud inválida", "La fecha tiene formato invalido", 400), None

    error_intervalo = validar_intervalo_reserva(inicio, fin)
    if error_intervalo is not None:
        return armar_error("BAD_REQUEST", "Solicitud inválida", error_intervalo, 400), None

    cancha = obtener_cancha_por_id(id_cancha)
    if cancha is None:
        return armar_error("NOT_FOUND", "Recurso no encontrado", "La cancha no existe", 404), None
    if not cancha['activa']:
        return armar_error("CONFLICT", "Conflicto de negocio", "La cancha no esta activa", 409), None

    socio = obtener_socio_por_id(id_socio)
    if socio is None:
        return armar_error("NOT_FOUND", "Recurso no encontrado", "El socio no existe", 404), None
    if not socio['activo']:
        return armar_error("CONFLICT", "Conflicto de negocio", "El socio no esta activo", 409), None

    if buscar_solapamientos("id_cancha", id_cancha, inicio, fin):
        return armar_error("CONFLICT", "Conflicto de negocio", "La cancha ya está reservada en ese horario", 409), None
    if buscar_solapamientos("id_socio", id_socio, inicio, fin):
        return armar_error("CONFLICT", "Conflicto de negocio", "El socio ya tiene una reserva en ese horario", 409), None

    return None, {"inicio": inicio, "fin": fin, "cancha": cancha, "socio": socio}

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
        return armar_error("BAD_REQUEST", "Solicitud inválida", error_estado, 400)

    reserva = obtener_reserva_por_id(reserva_id)
    if reserva is None:
        return armar_error("NOT_FOUND", "Recurso no encontrado", "La reserva no existe", 404)

    if nuevo_estado == reserva["estado"]:
        return None, 204

    transiciones_desde_actual = TRANSICIONES_PERMITIDAS.get(reserva["estado"])
    if transiciones_desde_actual is None:
        return armar_error("CONFLICT", "Conflicto de negocio", f"No se puede modificar una reserva en estado '{reserva['estado']}'", 409)

    condicion = transiciones_desde_actual.get(nuevo_estado)
    if condicion is None:
        return armar_error("CONFLICT", "Conflicto de negocio", f"No se puede pasar de '{reserva['estado']}' a '{nuevo_estado}'", 409)

    ahora = datetime.now(zona_horaria).replace(tzinfo=None)
    if not condicion(ahora, reserva["fecha_hora_inicio"], reserva["fecha_hora_fin"]):
        return armar_error("CONFLICT", "Conflicto de negocio", f"No se puede pasar a '{nuevo_estado}' en este momento", 409)

    actualizado = actualizar_estado(reserva_id, nuevo_estado)
    if not actualizado:
        return armar_error("INTERNAL_SERVER_ERROR", "Error interno del servidor", "No se pudo actualizar la reserva", 500)

    return None, 204

def armar_url_hateoas(base_url, limit, offset, filtros):
    params = []
    for clave, valor in filtros.items():
        if valor is not None:
            params.append(f"{clave}={valor}")
            
    params.append(f"_limit={str(limit)}")
    params.append(f"_offset={str(offset)}")
    
    query_string = "&".join(params)
    return {"href": f"{base_url}?{query_string}"}

def listar_reservas_service(id_cancha, id_socio, estado, fecha_desde, fecha_hasta, limit, offset, base_url):
    # Validar estado de peticion
    if estado is not None:
        error_estado = validar_estado(estado)
        if error_estado is not None:
            return armar_error("BAD_REQUEST", "Solicitud inválida", error_estado, 400)
    
    # obtener la lista y el conteo de BD
    reservas_db = listar_reservas(id_cancha, id_socio, estado, fecha_desde, fecha_hasta, limit, offset)
    total_registros = contar_reservas(id_cancha, id_socio, estado, fecha_desde, fecha_hasta)

    reservas = []
    for r in reservas_db:
        reservas.append({
            "id": int(r["id"]),
            "id_socio": int(r["id_socio"]),
            "id_cancha": int(r["id_cancha"]),
            "fecha_hora_inicio": formatear_fecha_hora(r["fecha_hora_inicio"]) if r.get("fecha_hora_inicio") else None,
            "fecha_hora_fin": formatear_fecha_hora(r["fecha_hora_fin"]) if r.get("fecha_hora_fin") else None,
            "estado": str(r["estado"]),
            "precio_hora": int(r["precio_hora"]),
            "precio_total": int(r["precio_total"])
        })

    # genera los links HATEOAS (_links)
    filtros = {
        "id_cancha": id_cancha,
        "id_socio": id_socio,
        "estado": estado,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    }

    last_offset = max(0, ((total_registros - 1) // limit) * limit) if total_registros > 0 else 0

    _links = {
        "_first": armar_url_hateoas(base_url, limit, 0, filtros),
        "_last": armar_url_hateoas(base_url, limit, last_offset, filtros)
    }

    if offset > 0:
        prev_offset = max(0, offset - limit)
        _links["_prev"] = armar_url_hateoas(base_url, limit, prev_offset, filtros)

    if offset + limit < total_registros:
        next_offset = offset + limit
        _links["_next"] = armar_url_hateoas(base_url, limit, next_offset, filtros)

    respuesta = {
        "reservas": reservas,
        "_links": _links
    }

    return respuesta, 200

def registrar_reservas_recurrentes(datos):
    # Validar formato
    cant_semanas = datos.get('cantidad_semanas')
    if type(cant_semanas) is not int or cant_semanas < 2 or cant_semanas > 12:
        return armar_error("BAD_REQUEST", "Solicitud inválida", "cantidad_semanas debe ser un entero entre 2 y 12", 400)

    inicio_base = parsear_fecha_hora(datos.get('fecha_hora_inicio'))
    fin_base = parsear_fecha_hora(datos.get('fecha_hora_fin'))
    if not inicio_base or not fin_base:
        return armar_error("BAD_REQUEST", "Solicitud inválida", "Formato de fecha invalido", 400)

    id_cancha = datos.get('id_cancha')
    id_socio = datos.get('id_socio')
    # Validar disponibilidad de cancha y existencia/actividad de socio
    cancha = obtener_cancha_por_id(id_cancha)
    if not cancha:
        return armar_error("NOT_FOUND", "Recurso no encontrado", "La cancha no existe", 404)
    if not cancha['activa']:
            return armar_error("CONFLICT", "Conflicto de negocio", "La cancha no esta activa", 409)

    socio = obtener_socio_por_id(id_socio)
    if not socio:
        return armar_error("NOT_FOUND", "Recurso no encontrado", "El socio no existe", 404)
    if not socio['activo']:
        return armar_error("CONFLICT", "Conflicto de negocio", "El socio no esta activo", 409)


    fechas_a_reservar = []
    conflictos = []
    # Verifica semana por semana segun la cantidad ingresada
    for i in range(cant_semanas):
        inicio_i = inicio_base + timedelta(weeks=i)
        fin_i = fin_base + timedelta(weeks=i)

        reserva_valida = validar_intervalo_reserva(inicio_i, fin_i)
        solap_cancha = buscar_solapamientos("id_cancha", id_cancha, inicio_i, fin_i)
        solap_socio = buscar_solapamientos("id_socio", id_socio, inicio_i, fin_i)

        if solap_cancha or solap_socio or reserva_valida is not None :
            conflictos.append(inicio_i.strftime("%Y-%m-%d"))
        else:
            fechas_a_reservar.append((inicio_i, fin_i))

    if conflictos:
        cuerpo, status = armar_error(
            "CONFLICT",
            "Conflicto de negocio",
            "No se pudo realizar la reserva recurrente por conflictos de horario",
            409
            )
        cuerpo["conflictos"] = conflictos
        return cuerpo, status

    reservas_creadas = []
    precio_hora = int(cancha['precio_hora'])
    for inicio_i, fin_i in fechas_a_reservar:    
        horas = ((fin_i - inicio_i).total_seconds())/3600
        precio_total = int(precio_hora * horas)
        datos_reserva = {
            "id_cancha": id_cancha,
            "id_socio": id_socio,
            "fecha_hora_inicio": formatear_fecha_hora(inicio_i),
            "fecha_hora_fin": formatear_fecha_hora(fin_i)
        }
        nuevo_id = crear_reserva(datos_reserva, precio_hora, precio_total)
        reserva = consultar_reserva_por_id(nuevo_id)
        reservas_creadas.append(reserva)
    return {"reservas": reservas_creadas}, 201