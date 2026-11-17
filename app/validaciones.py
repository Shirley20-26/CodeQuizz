import re
from datetime import date

USUARIO_RE = re.compile(r"^[A-Za-z0-9_]{3,20}$")
CORREO_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
EDAD_MIN = 7
EDAD_MAX = 100

# Cada función devuelve None si todo está bien, o un mensaje amigable si hay error.


def validar_usuario(usuario):
    if not USUARIO_RE.match(usuario):
        return "El usuario debe tener de 3 a 20 letras, números o guion bajo (_), sin espacios ni tildes."
    return None


def validar_correo(correo):
    if len(correo) > 100 or not CORREO_RE.match(correo):
        return "Escribe un correo válido, por ejemplo nombre@gmail.com."
    return None


def validar_clave(clave):
    if len(clave) < 8 or len(clave) > 64:
        return "La contraseña debe tener entre 8 y 64 caracteres."
    if not any(c.isalpha() for c in clave) or not any(c.isdigit() for c in clave):
        return "La contraseña debe tener al menos una letra y un número."
    return None


def calcular_edad(nacimiento, hoy=None):
    """Años cumplidos. Si todavía no llegó tu cumpleaños este año, resta uno."""
    hoy = hoy or date.today()
    return hoy.year - nacimiento.year - (
        (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day)
    )


def fase_de_edad(edad):
    """Etapa que le toca a cada edad. El usuario no la elige."""
    if edad <= 11:
        return "escuela"
    if edad <= 17:
        return "colegio"
    return "universidad"


def validar_fecha_nacimiento(dia_txt, mes_txt, anio_txt):
    """Devuelve (fecha, None) si está bien, o (None, mensaje) si hay error."""
    dia_txt, mes_txt, anio_txt = dia_txt.strip(), mes_txt.strip(), anio_txt.strip()

    if not (dia_txt.isdecimal() and mes_txt.isdecimal() and anio_txt.isdecimal()):
        return None, "Escribe tu fecha de nacimiento con números: día, mes y año."
    if len(dia_txt) > 2 or len(mes_txt) > 2 or len(anio_txt) != 4:
        return None, "Usa día (1 a 31), mes (1 a 12) y el año con 4 cifras."

    try:
        fecha = date(int(anio_txt), int(mes_txt), int(dia_txt))
    except ValueError:
        return None, "Esa fecha no existe. Revisa el día, el mes y el año."

    hoy = date.today()
    if fecha > hoy:
        return None, "La fecha de nacimiento no puede ser del futuro."

    edad = calcular_edad(fecha, hoy)
    if edad < EDAD_MIN:
        return None, f"CodeQuiz es para estudiantes desde los {EDAD_MIN} años."
    if edad > EDAD_MAX:
        return None, "Revisa el año de nacimiento."
    return fecha, None