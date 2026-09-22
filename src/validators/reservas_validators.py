CAMPOS_OBLIGATORIOS_CREATE = ['id_cancha', 'id_socio', 'fecha_hora_inicio', 'fecha_hora_fin', 'precio_hora', 'precio_total']
ESTADOS_VALIDOS = ("confirmada", "cancelada", "finalizada")


def validar_campos_creacion(datos):
    for campo in CAMPOS_OBLIGATORIOS_CREATE:
        if campo not in datos or datos[campo] is None or str(datos[campo]).strip() == "":
            return f"El campo '{campo}' es obligatorio."
    return None


def validar_estado(estado):
    if estado not in ESTADOS_VALIDOS:
        return "Estado desconocido"
    return None


def validar_cuerpo_cambio_estado(datos):
    if not isinstance(datos, dict) or set(datos.keys()) != {"estado"}:
        return "El cuerpo debe tener únicamente el campo 'estado'"
    return None