from src.repositories.reservas_repository import obtener_reserva_por_id

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
