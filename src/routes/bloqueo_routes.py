from flask import Blueprint, jsonify
from src.services.bloqueo_service import eliminar_bloqueo_service

bloqueos_bp = Blueprint('bloqueos',__name__)

@bloqueos_bp.route("/bloqueos/<int:bloqueo_id>", methods=["DELETE"])
def delete_bloqueo(bloqueo_id): 
    respuesta, codigo = eliminar_bloqueo_service(bloqueo_id)

    if codigo == 204:
        return "", 204

    return jsonify(respuesta), codigo