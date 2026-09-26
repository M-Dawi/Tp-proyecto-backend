from src.repositories.canchas_repository import obtener_canchas, crear_canchas as crear_canchas_repo



def listar_canchas(limit, offset):

    if limit < 1 or limit >100:
        return {"error": "El límite debe estar entre 1 y 100"}, 400

    if offset < 0:
        return {"error": "El offset no puede ser negativo"}, 400


    canchas = obtener_canchas(limit=limit, offset=offset)
    
    return{
        "canchas": canchas,
        "limit": limit,
        "offset": offset
     }, 200
def crear_canchas(datos):
    if datos is None:
        return {"error": "No se proporcionaron datos para crear la cancha"}, 400

    nombre = datos.get("nombre")
    id_deporte = datos.get("id_deporte")
    precio_hora = datos.get("precio_hora")
    techada = datos.get("techada", False)
    activa = datos.get("activa", True)

    if not nombre :
        return {"error": "El nombre de la cancha es obligatorio"}, 400
    if id_deporte is None:
        return {"error": "El 'id_deporte' es obligatorio"}, 400
    if precio_hora is None:
        return {"error": "El 'precio_hora' es obligatorio"}, 400
    if precio_hora <= 0:
        return {"error": "El 'precio_hora' debe ser un entero mayor a cero"}, 400

    cancha = crear_canchas_repo(nombre, id_deporte, precio_hora, techada, activa)

    return cancha, 201
    
