from repositoris.canchas import obtener_canchas



def listar_canchas(limit, offset):

    if limit < 1 or limit >100:
        return {"error": "El límite debe estar entre 1 y 100"}, 400

    if offset < 0:
        return {"error": "El offset no puede ser negativo"}, 400


    canchas = obtener_canchas(limit, offset)

    return{
        "canchas": canchas,
        "limit": limit,
        "offset": offset
     }, 200
