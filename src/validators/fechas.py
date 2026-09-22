import re
from datetime import datetime, timezone, timedelta

PATRON_FECHA = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{6})-03:00$"
)

GMT_MENOS_3 = timezone(timedelta(hours=-3))
HORA_APERTURA = 8
HORA_CIERRE = 23

DIAS_POR_MES = {
    1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31,
}


def _es_bisiesto(anio):
    if anio % 4 != 0:
        return False
    if anio % 100 != 0:
        return True
    return anio % 400 == 0


def _dias_en_mes(anio, mes):
    if mes == 2 and _es_bisiesto(anio):
        return 29
    return DIAS_POR_MES[mes]


def parsear_fecha_hora(cadena):
    # Devuelve un datetime con zona horaria GMT-3, o None si el formato es inválido
    if not isinstance(cadena, str):
        return None

    match = PATRON_FECHA.match(cadena)
    if match is None:
        return None

    anio, mes, dia, hora, minuto, segundo, microsegundo = (int(g) for g in match.groups())

    if mes < 1 or mes > 12:
        return None
    if dia < 1 or dia > _dias_en_mes(anio, mes):
        return None
    if hora > 23:
        return None
    if minuto > 59:
        return None
    if segundo > 59:
        return None

    return datetime(anio, mes, dia, hora, minuto, segundo, microsegundo, tzinfo=GMT_MENOS_3)


def formatear_fecha_hora(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "-03:00"


def validar_intervalo_reserva(inicio, fin):
    # Devuelve None si el intervalo es válido, o un mensaje de error si no lo es
    if inicio >= fin:
        return "fecha_hora_inicio debe ser anterior a fecha_hora_fin"

    if inicio.date() != fin.date():
        return "La reserva no puede atravesar la medianoche"

    if inicio.minute != 0 or inicio.second != 0 or inicio.microsecond != 0:
        return "fecha_hora_inicio debe caer en una hora en punto"
    if fin.minute != 0 or fin.second != 0 or fin.microsecond != 0:
        return "fecha_hora_fin debe caer en una hora en punto"

    if inicio.hour < HORA_APERTURA or fin.hour > HORA_CIERRE:
        return f"El horario debe estar entre {HORA_APERTURA}:00 y {HORA_CIERRE}:00"

    duracion_horas = (fin - inicio).total_seconds() / 3600
    if duracion_horas < 1 or duracion_horas > 3:
        return "La reserva debe durar entre 1 y 3 horas completas"

    ahora = datetime.now(GMT_MENOS_3)
    if inicio <= ahora:
        return "El inicio de la reserva debe ser posterior al momento actual"

    return None