from datetime import datetime
from src.repositories.reservas_repository import obtener_reserva_por_id, crear_reserva, actualizar_estado

def consultar_reserva_por_id(reserva_id):
    reserva = obtener_reserva_por_id(reserva_id)
    if not reserva:
        return None

    reserva['fecha_hora_inicio'] = reserva['fecha_hora_inicio'].strftime("%Y-%m-%dT%H:%M:%S.%f") + "-03:00"
    reserva['fecha_hora_fin'] = reserva['fecha_hora_fin'].strftime("%Y-%m-%dT%H:%M:%S.%f") + "-03:00"
    reserva['precio_hora'] = float(reserva['precio_hora'])
    reserva['precio_total'] = float(reserva['precio_total'])
    reserva['created_at'] = str(reserva['created_at'])

    return reserva

def registrar_reserva(datos):
    # Verifica campos obligatorios que deben venir en la petición
    campos_requeridos = ['id_cancha', 'id_socio', 'fecha', 'hora_inicio', 'hora_fin', 'monto_total']
    
    # Validar que no falte ninguno, si falta alguno devuelve error codigo 400
    for campo in campos_requeridos:
        if campo not in datos or datos[campo] is None or str(datos[campo]).strip() == "":
            return {"error": f"El campo '{campo}' es obligatorio."}, 400

    nuevo_id = crear_reserva(datos)
    
    nueva_reserva = consultar_reserva_por_id(nuevo_id)
    return nueva_reserva, 201

TRANSICIONES_PERMITIDAS = {
    "confirmada": {
        "cancelada": lambda ahora, inicio, fin: ahora < inicio,
        "finalizada": lambda ahora, inicio, fin: ahora >= fin,
    },
}
def cambiar_estado(reserva_id, nuevo_estado):
    if nuevo_estado not in ("confirmada", "cancelada", "finalizada"):
        return {"error": "Estado desconocido"}, 400

    reserva = obtener_reserva_por_id(reserva_id)
    if reserva is None:
        return {"error": "La reserva no existe"}, 404

    # Repetir el estado actual = éxito, sin tocar nada
    if nuevo_estado == reserva["estado"]:
        return None, 204

    transiciones_desde_actual = TRANSICIONES_PERMITIDAS.get(reserva["estado"])
    if transiciones_desde_actual is None:
        return {"error": f"No se puede modificar una reserva en estado '{reserva['estado']}'"}, 409

    condicion = transiciones_desde_actual.get(nuevo_estado)
    if condicion is None:
        return {"error": f"No se puede pasar de '{reserva['estado']}' a '{nuevo_estado}'"}, 409

    ahora = datetime.now()
    if not condicion(ahora, reserva["fecha_hora_inicio"], reserva["fecha_hora_fin"]):
        return {"error": f"No se puede pasar a '{nuevo_estado}' en este momento"}, 409

    actualizado = actualizar_estado(reserva_id, nuevo_estado)
    if not actualizado:
        return {"error": "No se pudo actualizar la reserva"}, 500

    return None, 204