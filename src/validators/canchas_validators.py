import re
from datetime import date

PATRON_HORA_EN_PUNTO = re.compile(r'^([01]\d|2[0-3]):00:00$')
CAMPOS_EDITABLES_PATCH = {"nombre", "precio_hora", "techada", "activa"}


def validar_campos_actualizacion(datos):
    if not isinstance(datos, dict) or not datos:
        return "El cuerpo no puede estar vacío."

    desconocidos = set(datos.keys()) - CAMPOS_EDITABLES_PATCH
    if desconocidos:
        return f"Campos desconocidos o no editables: {', '.join(sorted(desconocidos))}."

    if "nombre" in datos:
        nombre = datos["nombre"]
        if not isinstance(nombre, str) or not nombre.strip():
            return "El campo 'nombre' no puede quedar vacío."

    if "precio_hora" in datos:
        precio_hora = datos["precio_hora"]
        if isinstance(precio_hora, bool) or not isinstance(precio_hora, int) or precio_hora <= 0:
            return "El campo 'precio_hora' debe ser un entero mayor a cero."

    if "techada" in datos and not isinstance(datos["techada"], bool):
        return "El campo 'techada' debe ser booleano."

    if "activa" in datos and not isinstance(datos["activa"], bool):
        return "El campo 'activa' debe ser booleano."

    return None

def validar_disponibilidad(args):
    if args is None:
        return "Faltan parámetros obligatorios."

    fecha = args.get("fecha")
    hora_inicio = args.get("hora_inicio")
    hora_fin = args.get("hora_fin")

    if not fecha:
        return "El parámetro 'fecha' es obligatorio."
    if not hora_inicio:
        return "El parámetro 'hora_inicio' es obligatorio."
    if not hora_fin:
        return "El parámetro 'hora_fin' es obligatorio."

    try:
        date.fromisoformat(fecha)
    except (ValueError, TypeError):
        return "El parámetro 'fecha' debe tener el formato YYYY-MM-DD."

    if not PATRON_HORA_EN_PUNTO.match(hora_inicio):
        return "El parámetro 'hora_inicio' debe tener formato HH:00:00."
    if not PATRON_HORA_EN_PUNTO.match(hora_fin):
        return "El parámetro 'hora_fin' debe tener formato HH:00:00."
    if hora_inicio >= hora_fin:
        return "'hora_inicio' debe ser anterior a 'hora_fin'."

    if "id_deporte" in args and args["id_deporte"]:
        try:
            if int(args["id_deporte"]) < 1:
                return "El parámetro 'id_deporte' debe ser un entero positivo."
        except (TypeError, ValueError):
            return "El parámetro 'id_deporte' debe ser un entero."
            
    if args.get("techada") is not None and args["techada"] not in ("true", "false"):
        return "El parámetro 'techada' debe ser 'true' o 'false'."

    return None