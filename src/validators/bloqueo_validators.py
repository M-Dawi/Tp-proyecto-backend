from datetime import date
from src.services.errores import armar_error

PARAMETROS_PERMITIDOS = {"id_cancha", "fecha", "_limit", "_offset"}
CAMPOS_OBLIGATORIOS_CREATE = ["id_cancha", "fecha", "hora_inicio", "hora_fin", "motivo"]
CAMPOS_PERMITIDOS_CREATE = set(CAMPOS_OBLIGATORIOS_CREATE)

def validar_filtros_listado(args):
   
    desconocidos = set(args.keys()) - PARAMETROS_PERMITIDOS
    if desconocidos:
        return None, armar_error(
            "PARAMETRO_DESCONOCIDO",
            "Se recibieron parametros no soportados",
            f"Parametros invalidos: {', '.join(sorted(desconocidos))}",
            400
        )

    filtros = {"id_cancha": None, "fecha": None}

    # Validacion id_cancha
    id_cancha_raw = args.get("id_cancha")
    if id_cancha_raw is not None:
        if not id_cancha_raw.isdigit() or int(id_cancha_raw) <= 0:
            return None, armar_error(
                "VALOR_INVALIDO",
                "id_cancha invalido",
                "id_cancha debe ser un entero positivo",
                400
            )
        filtros["id_cancha"] = int(id_cancha_raw)

    # Validacion fecha (YYYY-MM-DD)
    fecha_raw = args.get("fecha")
    if fecha_raw is not None:
        try:
            date.fromisoformat(fecha_raw)
        except (ValueError, TypeError):
            return None, armar_error(
                "VALOR_INVALIDO",
                "Fecha invalida",
                "La fecha debe tener el formato YYYY-MM-DD",
                400
            )
        filtros["fecha"] = fecha_raw

    # Validacion paginacion
    limit_raw = args.get("_limit", "10")
    offset_raw = args.get("_offset", "0")

    if not limit_raw.isdigit() or not (1 <= int(limit_raw) <= 100):
        return None, armar_error(
            "VALOR_INVALIDO",
            "_limit invalido",
            "_limit debe ser un entero entre 1 y 100",
            400
        )

    if not offset_raw.isdigit() or int(offset_raw) < 0:
        return None, armar_error(
            "VALOR_INVALIDO",
            "_offset invalido",
            "_offset no puede ser negativo",
            400
        )

    filtros["limit"] = int(limit_raw)
    filtros["offset"] = int(offset_raw)

    return filtros, None

def validar_campos_creacion(datos):

    if not isinstance(datos, dict) or not datos:
        return None, armar_error(
            "CUERPO_INVALIDO",
            "El cuerpo no puede estar vacio",
            "Se esperaba un objeto JSON con los campos del bloqueo",
            400
        )

    desconocidos = set(datos.keys()) - CAMPOS_PERMITIDOS_CREATE
    if desconocidos:
        return None, armar_error(
            "CAMPO_DESCONOCIDO",
            "Se recibieron campos no soportados",
            f"Campos invalidos: {', '.join(sorted(desconocidos))}",
            400
        )

    for campo in CAMPOS_OBLIGATORIOS_CREATE:
        if campo not in datos or datos[campo] is None or str(datos[campo]).strip() == "":
            return None, armar_error(
                "CAMPO_FALTANTE",
                f"El campo '{campo}' es obligatorio",
                f"Falta el campo '{campo}' en el cuerpo",
                400
            )

    id_cancha = datos.get("id_cancha")
    if isinstance(id_cancha, bool) or not isinstance(id_cancha, int) or id_cancha <= 0:
        return None, armar_error(
            "VALOR_INVALIDO",
            "id_cancha invalido",
            "id_cancha debe ser un entero positivo",
            400
        )

    fecha_raw = datos.get("fecha")
    try:
        date.fromisoformat(fecha_raw)
    except (ValueError, TypeError):
        return None, armar_error(
            "VALOR_INVALIDO",
            "Fecha invalida",
            "La fecha debe tener el formato YYYY-MM-DD",
            400
        )

    if datos["hora_inicio"] >= datos["hora_fin"]:
        return None, armar_error(
            "VALOR_INVALIDO",
            "Intervalo horario invalido",
            "hora_inicio debe ser menor que hora_fin",
            400
        )

    return {
        "id_cancha": id_cancha,
        "fecha": fecha_raw,
        "hora_inicio": datos["hora_inicio"],
        "hora_fin": datos["hora_fin"],
        "motivo": datos["motivo"],
    }, None