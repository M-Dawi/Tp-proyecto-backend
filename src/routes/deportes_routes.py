from flask import Blueprint, jsonify
from src.repositories.deportes_repository import obtener_deportes
from src.services.errores import armar_error

deportes_bp = Blueprint('deportes', __name__)

@deportes_bp.route('/deportes', methods=['GET'])
def get_deportes():
    try:
        deportes = obtener_deportes()

    except Exception as e:
        print(f"Error al obtener deportes: {e}")
        cuerpo, status = armar_error("INTERNAL_SERVER_ERROR", "Error interno del servidor", "Ocurrió un error inesperado", 500)
        return jsonify(cuerpo), status

    if not deportes:
        return "", 204
    return jsonify({"deportes": deportes}), 200