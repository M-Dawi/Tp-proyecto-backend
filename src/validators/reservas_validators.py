from src.services.socios_service import armar_error

CAMPOS_OBLIGATORIOS_CREATE = ['id_cancha', 'id_socio', 'fecha_hora_inicio', 'fecha_hora_fin']
ESTADOS_VALIDOS = ("confirmada", "cancelada", "finalizada")

def validar_parametros_paginacion(limit, offset):
    if limit < 1 or limit > 100 or offset < 0:
        return armar_error(
            "PARAMETRO_INVALIDO",
            "Parametros de paginacion invalidos",
            "_limit debe estar entre 1 y 100, y _offset no puede ser negativo."
        )
    return None
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