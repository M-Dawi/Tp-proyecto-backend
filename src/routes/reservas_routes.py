from flask import Blueprint, jsonify, request
from src.services.reservas_service import consultar_reserva_por_id, registrar_reserva, cambiar_estado
from src.validators.reservas_validators import validar_cuerpo_cambio_estado

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def obtener_reserva(id):
    reserva = consultar_reserva_por_id(id)
    if not reserva:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404

    return jsonify(reserva), 200

@reservas_bp.route('/reservas', methods=['POST'])
def crear_nueva_reserva():
    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({"error": "Debe enviar un cuerpo en formato JSON"}), 400

    resultado, status_code = registrar_reserva(datos)

    return jsonify(resultado), status_code

@reservas_bp.route('/reservas/<int:id>/estado', methods=['PUT'])
def cambiar_estado_reserva(id):
    datos = request.get_json(silent=True)

    error_cuerpo = validar_cuerpo_cambio_estado(datos)
    if error_cuerpo is not None:
        return jsonify({"error": error_cuerpo}), 400

    resultado, status_code = cambiar_estado(id, datos["estado"])

    if status_code == 204:
        return "", 204

    return jsonify(resultado), status_code