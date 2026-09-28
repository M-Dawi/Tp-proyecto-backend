from flask import Blueprint, request, jsonify  # type: ignore[reportMissingImports]
from src.services.canchas_service import (
    listar_canchas, 
    crear_canchas,
    obtener_cancha, 
    actualizar_cancha,
    eliminar_cancha,
    listar_canchas_disponibles
)

from src.services.errores import armar_error

def _bad_request(descripcion):
    cuerpo, status = armar_error("BAD_REQUEST", "Solicitud inválida", descripcion, 400)
    return jsonify(cuerpo), status

canchas_bp = Blueprint('canchas',__name__)

@canchas_bp.route('/canchas', methods=['GET'])
def get_canchas():

    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except (TypeError, ValueError):
        return _bad_request("_limit y _offset deben ser enteros")

    resultado, codigo = listar_canchas(
        limit, offset,
        id_deporte=request.args.get('id_deporte', type=int),
        nombre=request.args.get('nombre'),
        techada=request.args.get('techada'),
        activa=request.args.get('activa'),
        base_url=request.base_url,
    )

    if codigo == 204:
        return "", 204

    return jsonify(resultado), codigo

@canchas_bp.route('/canchas/<int:cancha_id>', methods=['DELETE'])
def delete_cancha(cancha_id):
    resultado, codigo = eliminar_cancha(cancha_id)
    if codigo == 204:
        return "", 204
    return jsonify(resultado), codigo

@canchas_bp.route('/canchas', methods=['POST'])
def post_canchas():

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return _bad_request('No se proporcionaron datos')
    resultado, codigo = crear_canchas(datos)

    return jsonify(resultado), codigo


@canchas_bp.route('/canchas/<int:cancha_id>', methods=['GET'])
def get_cancha(cancha_id):
    resultado, codigo = obtener_cancha(cancha_id)
    return jsonify(resultado), codigo


@canchas_bp.route('/canchas/<int:cancha_id>', methods=['PATCH'])
def patch_cancha(cancha_id):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return _bad_request('No se proporcionaron datos')

    resultado, codigo = actualizar_cancha(cancha_id, datos)

    if codigo == 204:
        return "", 204

    return jsonify(resultado), codigo

@canchas_bp.route('/canchas/disponibles', methods=['GET'])
def get_canchas_disponibles():
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except (TypeError, ValueError):
        return _bad_request("_limit y _offset deben ser enteros")

    resultado, codigo = listar_canchas_disponibles(
        fecha=request.args.get('fecha'),
        hora_inicio=request.args.get('hora_inicio'),
        hora_fin=request.args.get('hora_fin'),
        id_deporte=request.args.get('id_deporte'),
        techada=request.args.get('techada'),
        limit=limit,
        offset=offset,
    )

    if codigo == 204:
        return "", 204

    return jsonify(resultado), codigo