from flask import Blueprint, jsonify, request
from src.services.reservas_service import consultar_reserva_por_id, registrar_reserva, cambiar_estado

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def obtener_reserva(id):
    reserva = consultar_reserva_por_id(id)
    if not reserva:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404
    
    return jsonify(reserva), 200

@reservas_bp.route('/reservas', methods=['POST'])
def crear_nueva_reserva():
    datos = request.get_json()
    
    # Validar que sea formato json
    if not datos:
        return jsonify({"error": "Debe enviar un cuerpo en formato JSON"}), 400
    
    # Llama al servicio para procesar la creación y validación de la reserva
    resultado, status_code = registrar_reserva(datos)
    
    return jsonify(resultado), status_code

@reservas_bp.route('/reservas/<int:id>/estado', methods=['PUT'])
def cambiar_estado_reserva(id):
    datos = request.get_json()

    if not isinstance(datos, dict) or set(datos.keys()) != {"estado"}:
        return jsonify({"error": "El cuerpo debe tener únicamente el campo 'estado'"}), 400

    resultado, status_code = cambiar_estado(id, datos["estado"])

    if status_code == 204:
        return "", 204

    return jsonify(resultado), status_code