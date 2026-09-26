from flask import Blueprint, jsonify, request
from src.services.reservas_service import consultar_reserva_por_id, registrar_reserva, cambiar_estado
from src.validators.reservas_validators import validar_cuerpo_cambio_estado
from src.validators.reservas_validators import validar_parametros_paginacion
from src.services.reservas_service import listar_reservas_service

reservas_bp = Blueprint('reservas', __name__)

# Listar reservas ------------------
@reservas_bp.route('/reservas', methods=['GET'])
def obtener_reservas():
  
    id_cancha = request.args.get('id_cancha', type=int)
    id_socio = request.args.get('id_socio', type=int)
    estado = request.args.get('estado', type=str)
    fecha_desde = request.args.get('fecha_desde', type=str)
    fecha_hasta = request.args.get('fecha_hasta', type=str)

   
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)

    error_paginacion = validar_parametros_paginacion(limit, offset)
    if error_paginacion:
        return jsonify(error_paginacion), 400
  
    resultado, status_code = listar_reservas_service(
        id_cancha=id_cancha,
        id_socio=id_socio,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limit=limit,
        offset=offset,
        base_url=request.base_url
    )

    return jsonify(resultado), status_code

#Obtener  una reserva por id ---------------
@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def obtener_reserva(id):
    reserva = consultar_reserva_por_id(id)
    if not reserva:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404

    return jsonify(reserva), 200

#Crear una reserva --------------------
@reservas_bp.route('/reservas', methods=['POST'])
def crear_nueva_reserva():
    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({"error": "Debe enviar un cuerpo en formato JSON"}), 400

    resultado, status_code = registrar_reserva(datos)

    return jsonify(resultado), status_code

#Establecer el estado de una reserva --------------------
@reservas_bp.route('/reservas/<int:id>/estado', methods=['PUT'])
def cambiar_estado_reserva(id):
    datos = request.get_json(silent=True)

    error_cuerpo = validar_cuerpo_cambio_estado(datos)
    if error_cuerpo is not None:
        return jsonify({"error": error_cuerpo}), 400

    resultado, status_code = cambiar_estado(id, datos["estado"])

    if status_code == 204:
        return "", 204

    return jsonify(resultado), status_code