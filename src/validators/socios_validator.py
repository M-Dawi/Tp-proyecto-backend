def validar_datos_crear_socio(cuerpo):

    if not cuerpo or not isinstance(cuerpo, dict):
        return "El cuerpo debe ser un objeto JSON (diccionario) no vacío."
    
    campos_recibidos = set(cuerpo.keys())
    campos_permitidos = {"nombre", "email"}

    if campos_recibidos != campos_permitidos:
        return "El JSON debe contener exactamente los campos 'nombre' y 'email'."

    nombre = cuerpo.get("nombre")
    email = cuerpo.get("email")

    if not isinstance(nombre, str) or not isinstance(email, str):
        return "Los campos 'nombre' y 'email' deben ser texto."

    nombre_limpio = nombre.strip()

    if nombre_limpio == "":
        return "El nombre no puede estar vacío."

    email_limpio = email.strip().lower()

    if email_limpio.count("@") != 1:
        return "El formato de email no es valido"

    if email_limpio.count(" ") >= 1:
        return "El formato de email no es valido"

    usuario, dominio = email_limpio.split("@")

    if not usuario or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        return "El formato de email no es valido"

    return None

def validar_datos_actualizar_socio(cuerpo):

    if not isinstance(cuerpo, dict):
        return "El cuerpo debe ser un objeto JSON (diccionario)."

    if cuerpo == {}:
        return "El cuerpo no puede estar vacío."

    campos_recibidos = set(cuerpo.keys())
    campos_permitidos = {"nombre", "email", "activo"}

    campos_no_permitidos = campos_recibidos - campos_permitidos

    if campos_no_permitidos:
        return "El JSON solo puede contener los campos 'nombre', 'email' y 'activo'."

    if "nombre" in cuerpo:
        nombre = cuerpo.get("nombre")

        if not isinstance(nombre, str):
            return "El campo 'nombre' debe ser texto."

        nombre_limpio = nombre.strip()
        if nombre_limpio == "":
            return "El nombre no puede estar vacío."

    if "email" in cuerpo:
        email = cuerpo.get("email")
        if not isinstance(email, str):
            return "El campo 'email' debe ser texto."

        email_limpio = email.strip().lower()
        if email_limpio.count("@") != 1:
            return "El formato de email no es valido"
        if email_limpio.count(" ") >= 1:
            return "El formato de email no es valido"

        usuario, dominio = email_limpio.split("@")
        if not usuario or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
            return "El formato de email no es valido"        

    if "activo" in cuerpo:
        activo = cuerpo.get("activo")
        if not isinstance(activo, bool):
            return "El campo 'activo' debe ser booleano."

    return None
    