from flask import Blueprint,jsonify
from src.repositories.deportes_repository import obtener_deportes

deportes_bp = Blueprint('deportes', __name__)
@deportes_bp.route('/deportes', methods=['GET'])
def get_deportes():
    deportes = obtener_deportes()
    return jsonify({"deportes": deportes}), 200

