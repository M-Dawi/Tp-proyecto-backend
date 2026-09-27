from flask import Blueprint, jsonify, request
from src.services.bloqueo_service import crear_bloqueo_service, eliminar_bloqueo_service, obtener_bloqueos_service
from src.validators.bloqueo_validators import validar_filtros_listado, validar_campos_creacion

bloqueos_bp = Blueprint('bloqueos', __name__)


@bloqueos_bp.route("/bloqueos", methods=["GET"])
def get_bloqueo():
    filtros, error = validar_filtros_listado(request.args)
    if error:
        cuerpo, codigo = error
        return jsonify(cuerpo), codigo
    respuesta, codigo = obtener_bloqueos_service(filtros, request.base_url)
    return jsonify(respuesta), codigo


@bloqueos_bp.route("/bloqueos", methods=["POST"])
def create_bloqueo():
    datos = request.get_json(silent=True)

    datos_validados, error = validar_campos_creacion(datos)
    if error:
        cuerpo, codigo = error
        return jsonify(cuerpo), codigo

    resultado, codigo = crear_bloqueo_service(datos_validados)
    return jsonify(resultado), codigo


@bloqueos_bp.route("/bloqueos/<int:bloqueo_id>", methods=["DELETE"])
def delete_bloqueo(bloqueo_id):
    respuesta, codigo = eliminar_bloqueo_service(bloqueo_id)
    if codigo == 204:
        return "", 204
    return jsonify(respuesta), codigo