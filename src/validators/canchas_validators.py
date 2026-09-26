CAMPOS_EDITABLES_PATCH = {'nombre', 'precio_hora', 'techada', 'activa'}


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