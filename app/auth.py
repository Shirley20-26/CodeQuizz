import sqlite3
import time
from datetime import date
from app import db, seguridad
from app import validaciones as v

MAX_INTENTOS = 5
BLOQUEO_SEGUNDOS = 300  

MENSAJE_LOGIN = "Usuario o contraseña incorrectos."
MENSAJE_RECUPERAR = "Usuario o código de recuperación incorrectos."

_actual = None  




def _publico(fila):
    edad = v.calcular_edad(date.fromisoformat(fila["fecha_nacimiento"]))
    return {
        "id": fila["id"],
        "usuario": fila["usuario"],
        "correo": fila["correo"],
        "edad": edad,
        "fase": v.fase_de_edad(edad),
        "rol": fila["rol"],
    }


def _segundos_de_bloqueo(fila):
    restante = fila["bloqueado_hasta"] - time.time()
    return int(restante) + 1 if restante > 0 else 0


def _texto_bloqueo(segundos):
    minutos = max(1, (segundos + 59) // 60)
    return f"Demasiados intentos. Intenta de nuevo en {minutos} min."


def _registrar_fallo(fila):
    intentos = fila["intentos_fallidos"] + 1
    bloqueo = 0
    if intentos >= MAX_INTENTOS:
        bloqueo = time.time() + BLOQUEO_SEGUNDOS
        intentos = 0
    db.ejecutar(
        "UPDATE usuarios SET intentos_fallidos = ?, bloqueado_hasta = ? WHERE id = ?",
        (intentos, bloqueo, fila["id"]),
    )


def _limpiar_fallos(usuario_id):
    db.ejecutar(
        "UPDATE usuarios SET intentos_fallidos = 0, bloqueado_hasta = 0 WHERE id = ?",
        (usuario_id,),
    )


def _abrir_sesion(fila):
    global _actual
    db.ejecutar(
        "INSERT OR REPLACE INTO sesion (id, usuario_id, token, iniciada) "
        "VALUES (1, ?, ?, ?)",
        (fila["id"], seguridad.generar_token(), time.time()),
    )
    _actual = _publico(fila)




def registrar(usuario, correo, dia, mes, anio, clave, clave2):
    """Devuelve (True, codigo_recuperacion) o (False, mensaje_de_error)."""
    usuario = usuario.strip()
    correo = correo.strip().lower()

    error = v.validar_usuario(usuario) or v.validar_correo(correo)
    if error:
        return False, error

    fecha, error = v.validar_fecha_nacimiento(dia, mes, anio)
    if error:
        return False, error

    error = v.validar_clave(clave)
    if error:
        return False, error
    if clave != clave2:
        return False, "Las contraseñas no coinciden."

    existe = db.uno(
        "SELECT 1 FROM usuarios WHERE usuario = ? OR correo = ?", (usuario, correo)
    )
    if existe:
        return False, "Ese usuario o correo ya está registrado."

    codigo = seguridad.generar_codigo_recuperacion()
    try:
        nuevo_id = db.ejecutar(
            "INSERT INTO usuarios (usuario, correo, fecha_nacimiento, hash_clave, "
            "hash_recuperacion, creado) VALUES (?, ?, ?, ?, ?, ?)",
            (
                usuario,
                correo,
                fecha.isoformat(),
                seguridad.hashear(clave),
                seguridad.hashear(seguridad.normalizar_codigo(codigo)),
                time.time(),
            ),
        )
    except sqlite3.IntegrityError:
        return False, "Ese usuario o correo ya está registrado."

    _abrir_sesion(db.uno("SELECT * FROM usuarios WHERE id = ?", (nuevo_id,)))
    return True, codigo


def iniciar_sesion(identificador, clave):
    """Entra con usuario o correo. Devuelve (True, "") o (False, mensaje)."""
    identificador = identificador.strip()
    if not identificador or not clave:
        return False, "Escribe tu usuario (o correo) y tu contraseña."

    fila = db.uno(
        "SELECT * FROM usuarios WHERE usuario = ? OR correo = ?",
        (identificador, identificador.lower()),
    )
    if fila is None:
        return False, MENSAJE_LOGIN  

    espera = _segundos_de_bloqueo(fila)
    if espera:
        return False, _texto_bloqueo(espera)

    if not seguridad.verificar(clave, fila["hash_clave"]):
        _registrar_fallo(fila)
        return False, MENSAJE_LOGIN

    _limpiar_fallos(fila["id"])
    _abrir_sesion(fila)
    return True, ""


def recuperar_clave(usuario, codigo, clave_nueva, clave2):
    """Cambia la contraseña usando el código de recuperación.
    Devuelve (True, codigo_nuevo) o (False, mensaje)."""
    error = v.validar_clave(clave_nueva)
    if error:
        return False, error
    if clave_nueva != clave2:
        return False, "Las contraseñas no coinciden."

    fila = db.uno("SELECT * FROM usuarios WHERE usuario = ?", (usuario.strip(),))
    if fila is None:
        return False, MENSAJE_RECUPERAR

    espera = _segundos_de_bloqueo(fila)
    if espera:
        return False, _texto_bloqueo(espera)

    codigo_limpio = seguridad.normalizar_codigo(codigo)
    if not seguridad.verificar(codigo_limpio, fila["hash_recuperacion"]):
        _registrar_fallo(fila)
        return False, MENSAJE_RECUPERAR

    codigo_nuevo = seguridad.generar_codigo_recuperacion()
    db.ejecutar(
        "UPDATE usuarios SET hash_clave = ?, hash_recuperacion = ?, "
        "intentos_fallidos = 0, bloqueado_hasta = 0 WHERE id = ?",
        (
            seguridad.hashear(clave_nueva),
            seguridad.hashear(seguridad.normalizar_codigo(codigo_nuevo)),
            fila["id"],
        ),
    )
    db.ejecutar("DELETE FROM sesion WHERE usuario_id = ?", (fila["id"],))
    return True, codigo_nuevo


def restaurar_sesion():
    """Al abrir la app: si había una sesión guardada, entra solo (sin internet)."""
    global _actual
    fila = db.uno(
        "SELECT u.* FROM sesion s JOIN usuarios u ON u.id = s.usuario_id WHERE s.id = 1"
    )
    _actual = _publico(fila) if fila else None
    return _actual is not None


def cerrar_sesion():
    global _actual
    db.ejecutar("DELETE FROM sesion")
    _actual = None


def usuario_actual():
    """Devuelve los datos públicos del usuario, o None si es invitado."""
    return _actual