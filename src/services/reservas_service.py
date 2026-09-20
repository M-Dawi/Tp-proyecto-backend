from src.repositories.reservas_repository import obtener_reserva_por_id, crear_reserva

def consultar_reserva_por_id(reserva_id):
    reserva = obtener_reserva_por_id(reserva_id)
    if not reserva:
        return None
    
    # Convierte objetos de fecha, hora y monto a string y float para que sea compatible con json
    reserva['fecha'] = str(reserva['fecha'])
    reserva['hora_inicio'] = str(reserva['hora_inicio'])
    reserva['hora_fin'] = str(reserva['hora_fin'])
    reserva['monto_total'] = float(reserva['monto_total'])
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
