from flask import Blueprint, jsonify, request
from src.services.socios_service import (crear_socio_service, actualizar_socio_service, obtener_socios_service, obtener_socio_por_id_service)

socios_bp = Blueprint('socios',__name__)

@socios_bp.route("/socios", methods=["GET"])
def get_socios():
    nombre = request.args.get("nombre")
    activo = request.args.get("activo")
    limit = request.args.get("_limit", 10, type=int)
    offset = request.args.get("_offset", 0, type=int)

    respuesta, codigo = obtener_socios_service(limit, offset, nombre, activo)
    return jsonify(respuesta), codigo

@socios_bp.route("/socios/<int:socio_id>", methods=["GET"])
def get_socio_por_id(socio_id): 
    respuesta, codigo = obtener_socio_por_id_service(socio_id)
    return jsonify(respuesta), codigo

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