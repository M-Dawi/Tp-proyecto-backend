from flask import Blueprint, request, jsonify
from services.canchas import listar_canchas

canchas_bp = Blueprint('canchas',__name__)

@canchas_bp.route('/canchas', methods=['GET'])
def get_canchas():


    limit = int(request.args.get('_limit', 10))
    offset = int(request.args.get('_offset', 0))


    resultado, codigo = listar_canchas(limit, offset)

    return jsonify(resultado), codigo