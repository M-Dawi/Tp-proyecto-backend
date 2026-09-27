from flask import Blueprint, jsonify, request
from src.services.bloqueo_service import crear_bloqueo, eliminar_bloqueo_service, obtener_bloqueos_service
from src.validators.bloqueo_validators import validar_filtros_listado

bloqueos_bp = Blueprint('bloqueos',__name__)

@bloqueos_bp.route("/bloqueos", methods=["GET"])
def get_bloqueo():
    filtros, error = validar_filtros_listado(request.args)
    if error:
        cuerpo, codigo = error
        return jsonify(cuerpo), codigo
    repuesta, codigo = obtener_bloqueos_service(filtros, request.base_url)
    return jsonify(repuesta), codigo

@bloqueos_bp.route("/bloqueos", methods=["POST"])
def create_bloqueo():
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    cancha_id = datos.get("cancha_id")
    fecha = datos.get("fecha")
    horario_de_inicio = datos.get("horario_de_inicio")
    horario_de_fin = datos.get("horario_de_fin")
    motivo = datos.get("motivo")

    if not cancha_id or not fecha or not horario_de_inicio or not horario_de_fin or not motivo:
        return jsonify({"error": "Faltan datos requeridos"}), 400
    cancha = cancha.query.get(cancha_id)
    if not cancha:
        return jsonify({"error": "La cancha especificada no existe"}), 404
    bloqueo = crear_bloqueo(cancha_id, fecha, horario_de_inicio, horario_de_fin, motivo)
    return jsonify({"message": "Bloqueo creado exitosamente", "bloqueo_id": bloqueo}), 201


@bloqueos_bp.route("/bloqueos/<int:bloqueo_id>", methods=["DELETE"])
def delete_bloqueo(bloqueo_id): 
    respuesta, codigo = eliminar_bloqueo_service(bloqueo_id)

    if codigo == 204:
        return "", 204

    
    return jsonify(respuesta), codigo
        