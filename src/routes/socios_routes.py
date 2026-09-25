from flask import Blueprint, jsonify, request
from src.services.socios_service import (crear_socio_service, actualizar_socio_service, obtener_socios_service, obtener_socio_por_id_service, armar_error, leer_paginacion)

socios_bp = Blueprint('socios',__name__)

@socios_bp.route("/socios", methods=["GET"])
def get_socios():
    recibidos = set(request.args.keys())
    permitidos = {"nombre", "activo", "_limit", "_offset"}
    parametros_no_permitidos = recibidos - permitidos

    if parametros_no_permitidos:
        error, codigo = armar_error("BAD_REQUEST", "Solicitud inválida", f"Parámetros no permitidos: {', '.join(parametros_no_permitidos)}", 400)
        return jsonify(error), codigo
    paginacion = leer_paginacion(request.args)
    if paginacion is None:
        error, codigo = armar_error("BAD_REQUEST", "Solicitud inválida", "Parámetros de paginación inválidos. _limit debe estar entre 1 y 100, y _offset debe ser mayor o igual a 0.", 400)
        return jsonify(error), codigo
    limit, offset = paginacion

    nombre = request.args.get("nombre", type=str)
    activo = request.args.get("activo")
        
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

    if codigo == 204:
        return None, 204

    return jsonify(respuesta), codigo