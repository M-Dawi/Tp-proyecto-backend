from flask import Blueprint, request, jsonify  # type: ignore[reportMissingImports]
from src.services.canchas_service import listar_canchas, crear_canchas # type: ignore

canchas_bp = Blueprint('canchas',__name__)

@canchas_bp.route('/canchas', methods=['GET'])
def get_canchas():


    limit = int(request.args.get('_limit', 10))
    offset = int(request.args.get('_offset', 0))


    resultado, codigo = listar_canchas(limit, offset)

    return jsonify(resultado), codigo

@canchas_bp.route('/canchas', methods=['POST'])
def post_canchas():

    datos = request.get_json()

    if datos is None:
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    resultado, codigo = crear_canchas(datos)

    return jsonify(resultado), codigo

