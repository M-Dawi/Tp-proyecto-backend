from flask import Blueprint, jsonify, request
from src.services.socios_service import crear_socio_service, actualizar_socio_service

socios_bp = Blueprint('socios',__name__)

@socios_bp.route("/socios", methods=["POST"])
def post_socios():
    cuerpo = request.get_json(silent=True)
    respuesta, codigo = crear_socio_service(cuerpo)
    return jsonify(respuesta), codigo

@socios_bp.route("/socios/<int:socio_id>", methods=['PATCH'])
def patch_socios(socio_id):
    cuerpo = request.get_json(silent=True)
    respuesta, codigo = actualizar_socio_service(socio_id, cuerpo)
    return jsonify(respuesta), codigo
