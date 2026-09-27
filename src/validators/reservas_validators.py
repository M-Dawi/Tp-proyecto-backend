CAMPOS_OBLIGATORIOS_CREATE = ['id_cancha', 'id_socio', 'fecha_hora_inicio', 'fecha_hora_fin']
ESTADOS_VALIDOS = ("confirmada", "cancelada", "finalizada")


def validar_parametros_paginacion(limit, offset):
    if limit < 1 or limit > 100 or offset < 0:
        return "_limit debe estar entre 1 y 100, y _offset no puede ser negativo."
    return None


def validar_campos_creacion(datos):
    if not isinstance(datos, dict):
        return "El cuerpo debe ser un objeto JSON."

    for campo in CAMPOS_OBLIGATORIOS_CREATE:
        if campo not in datos or datos[campo] is None or str(datos[campo]).strip() == "":
            return f"El campo '{campo}' es obligatorio."

    for campo in ("id_cancha", "id_socio"):
        valor = datos[campo]
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            return f"El campo '{campo}' debe ser un entero positivo."

    return None


def validar_estado(estado):
    if estado not in ESTADOS_VALIDOS:
        return "Estado desconocido"
    return None


def validar_cuerpo_cambio_estado(datos):
    if not isinstance(datos, dict) or set(datos.keys()) != {"estado"}:
        return "El cuerpo debe tener únicamente el campo 'estado'"
    return None