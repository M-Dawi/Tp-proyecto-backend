from src.repositories.bloqueo_repository import (
    obtener_bloqueo_por_id, eliminar_bloqueo
)
from src.services.errores import armar_error

def eliminar_bloqueo_service(bloqueo_id):
    try:
        bloqueo = obtener_bloqueo_por_id(bloqueo_id)
        if bloqueo is None:
            return armar_error(            
                    "NOT_FOUND", 
                    "Recurso no encontrado",    
                    "No se encuentra bloqueo en nuestra base de datos", 
                    404
                    )
        esta_bloqueado = eliminar_bloqueo(bloqueo_id)
        if esta_bloqueado:
            return None, 204
        else:
            return armar_error(
                "INTERNAL_SERVER_ERROR", 
                "Error interno del servidor", 
                "Error de conexión al eliminar bloqueo",
                500
            )
    except Exception as e:
        print("Error:", e)
        return armar_error(
            "INTERNAL_SERVER_ERROR", 
            "Error interno del servidor", 
            "Ocurrió un error inesperado",
            500
        )