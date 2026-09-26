def armar_error(code, message, description, status_code):
    return {
        "errors": [
            {
                "code": code,
                "message": message,
                "level": "error",
                "description": description
            }
        ]
    }, status_code