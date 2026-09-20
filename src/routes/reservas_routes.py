from flask import Blueprint, jsonify
from src.services.reservas_service import consultar_reserva_por_id

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def obtener_reserva(id):
    reserva = consultar_reserva_por_id(id)
    if not reserva:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404
    
    return jsonify(reserva), 200
