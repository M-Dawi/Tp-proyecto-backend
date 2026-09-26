# Proyecto Backend - Sistema de Reservas de Club Deportivo

## Integrantes

| Nombre | Padrón |
|--------|--------|
| Mateo Dawidiuk | 114814 |
| Nicolas Wu | 116072 |
| Ian Acosta | 115494 |
| Evelyn Pamela Julian Flores | 110787 |
| Héctor Bustamante | 115963 |
| Cristy Mar Contreras Colmenares | 116104 |
| Luz Maria Moreno Benitez | 116373 |
| Milena Moreyra Taburet | 116327 |
| Nahuel Plasencia | 116072 |

## Estructura del proyecto

```
Tp-proyecto-backend/
├── app.py
├── .gitignore
├── README.md
├── requirements.txt                       # Dependencias Python.
├── src/
│   ├── repositories/
│   │   ├── canchas_repository.py          # Funciones para conectar con base de datos de canchas. Sentencias SQL.
│   │   └── deportes_repository.py         # Funciones para conectar con base de datos de deportes. Sentencias SQL.
│   │   └── reservas_repository.py         # Funciones para conectar con base de datos de reservas. Sentencias SQL.
│   │   └── socios_repository.py           # Funciones para conectar con base de datos de socios. Sentencias SQL.
│   ├── routes/
│   │   ├── canchas_routes.py              # Endpoints REST de canchas.
│   │   └── deportes_routes.py             # Endpoints REST de deportes.
│   │   └── reservas_routes.py             # Endpoints REST de reservas.
│   │   └── socios_routes.py               # Endpoints REST de socios.
│   ├── services/
│   │   ├── canchas_services.py            # Logica de negocio de canchas.
│   │   └── reservas_services.py           # Logica de negocio de reservas.
│   │   └── socios_services.py             # Logica de negocio de socios.
│   └── validators/
│       ├── fechas.py                      # Validacion de entrada para fechas.
│       └── reservas_validators.py         # Validacion de entrada para reservas.
│       └── socios_validators.py           # Validacion de entrada para socios.
├── db/
│   └── init.sql
│   └── db.py
└── docs/
    └── swagger.yaml
```

## Versiones utilizadas

*Dependencias principales* (ver `requirements.txt` para la lista completa):

- Python 3.14.4 (verificar con `python3 --version`)
- Flask 3.1.3
- mysql-connector-python 26.7.0
- MYSQL 8.0

## Documentación (Swagger / OpenAPI)

La especificación completa de la API en formato OpenAPI 3.0 está en [`docs/swagger.yaml`](docs/swagger.yaml). Se puede visualizar:

- Pegando el contenido del archivo en [editor.swagger.io](https://editor.swagger.io).
- Con una extensión tipo "Swagger Viewer" en VS Code.

## Instalación y ejecución

- 1. Clonar el repositorio
- 2. Crear entorno virtual:
```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
```
- 3. Instalar dependencias:
```bash
   pip install -r requirements.txt
```
- 4. Copiar .env.example a .env y completar con tus credenciales de MySQL
- 5. Crear la base de datos y las tablas:
```bash
   mysql -u tu_usuario -p < db/init.sql
```
- 6. Ejecutar la aplicación:
```bash
   python app.py
```
- 7. La API queda disponible en http://127.0.0.1:5000

## Ejemplos de uso

### Crear una reserva
```bash
curl -X POST http://127.0.0.1:5000/reservas \\
  -H "Content-Type: application/json" \\
  -d '{"id_socio": 1, "id_cancha": 1, "fecha_hora_inicio": "2026-12-01T18:00:00.000000-03:00", "fecha_hora_fin": "2026-12-01T20:00:00.000000-03:00"}'
```

### Cambiar el estado de una reserva
```bash
curl -X PUT http://127.0.0.1:5000/reservas/1/estado \\
  -H "Content-Type: application/json" \\
  -d '{"estado": "cancelada"}'
```

## Supuestos adoptados

- Los horarios se interpretan en GMT-3 (`-03:00`), sin conversión de zona horaria.
- El club atiende todos los días de 08:00 a 23:00, sin excepciones por feriados.
- Las reservas duran entre 1 y 3 horas completas, comienzan y terminan en horas en punto y no cruzan la medianoche.
- Los precios se expresan como enteros en centavos (por ejemplo, `1000000` representa $10.000,00).
- Al crear una reserva se conserva la tarifa vigente y el total calculado, aunque después cambie el precio de la cancha.
- Se rechaza una reserva si la cancha o el socio están inactivos, respondiendo 409.
- El filtro de fechas del listado de reservas (`fecha_desde` / `fecha_hasta`) se aplica sobre el día de la reserva.
- El formato de email válido se definió como: un solo `@`, texto antes y después, sin espacios, y un punto en el dominio que no esté al principio ni al final.
- Un email ya registrado bloquea el alta o la edición aunque el socio que lo tiene esté inactivo.
- No se valida explícitamente que el `id` de la URL sea positivo: un `id` inexistente responde 404, y uno negativo no matchea la ruta.

## Estado de la implementación

- **Deportes**: implementado (GET).
- **Socios**: implementado (listado con filtros y paginación, alta, consulta por id, actualización).
- **Reservas**: alta (POST) con todas las validaciones, consulta por id, cambio de estado y listado. 
- **Canchas**: listado y alta implementados; pendientes GET por id, PATCH, DELETE y disponibilidad.
- **Extensiones opcionales** (bloqueos por mantenimiento y reservas recurrentes): no implementadas.