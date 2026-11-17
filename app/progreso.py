from app import auth, db
from app.catalogo import aprobado, existe_nivel


def _usuario():
    return auth.usuario_actual()


def nivel_desbloqueado(fase, tema, nivel):
    """El nivel 1 siempre está abierto; los demás piden superar el anterior."""
    if nivel <= 1:
        return True
    return estado_nivel(fase, tema, nivel - 1)["superado"]


def puede_jugar(fase, tema, nivel):
    """Reglas de acceso:
    - El invitado solo puede jugar la demo.
    - Cada usuario solo juega su propia etapa y los niveles ya desbloqueados."""
    usuario = _usuario()
    if usuario is None:
        return (fase, tema, nivel) == ("invitado", "demo", 1)
    if fase != usuario["fase"] or not existe_nivel(fase, tema, nivel):
        return False
    return nivel_desbloqueado(fase, tema, nivel)


def estado_nivel(fase, tema, nivel):
    vacio = {"superado": False, "mejor_puntaje": 0, "mejor_aciertos": 0, "intentos": 0}
    usuario = _usuario()
    if usuario is None:
        return vacio
    fila = db.uno(
        "SELECT * FROM progreso WHERE usuario_id = ? AND fase = ? AND tema = ? AND nivel = ?",
        (usuario["id"], fase, tema, nivel),
    )
    if fila is None:
        return vacio
    return {
        "superado": bool(fila["superado"]),
        "mejor_puntaje": fila["mejor_puntaje"],
        "mejor_aciertos": fila["mejor_aciertos"],
        "intentos": fila["intentos"],
    }


def guardar_resultado(fase, tema, nivel, puntos, aciertos, total):
    """Guarda la partida del usuario con sesión. El invitado no guarda nada."""
    superado_ahora = aprobado(aciertos, total)
    usuario = _usuario()

    if usuario is None or fase != usuario["fase"]:
        return {
            "guardado": False, "superado": superado_ahora,
            "tiene_medalla": False, "medalla_nueva": False, "record": False,
        }

    uid = usuario["id"]
    fila = db.uno(
        "SELECT * FROM progreso WHERE usuario_id = ? AND fase = ? AND tema = ? AND nivel = ?",
        (uid, fase, tema, nivel),
    )

    if fila is None:
        db.ejecutar(
            "INSERT INTO progreso (usuario_id, fase, tema, nivel, mejor_puntaje, "
            "mejor_aciertos, intentos, superado) VALUES (?, ?, ?, ?, ?, ?, 1, ?)",
            (uid, fase, tema, nivel, puntos, aciertos, int(superado_ahora)),
        )
        ya_tenia = False
        record = False
    else:
        ya_tenia = bool(fila["superado"])
        record = puntos > fila["mejor_puntaje"]
        db.ejecutar(
            "UPDATE progreso SET mejor_puntaje = ?, mejor_aciertos = ?, "
            "intentos = intentos + 1, superado = ? "
            "WHERE usuario_id = ? AND fase = ? AND tema = ? AND nivel = ?",
            (
                max(fila["mejor_puntaje"], puntos),
                max(fila["mejor_aciertos"], aciertos),
                int(ya_tenia or superado_ahora),
                uid, fase, tema, nivel,
            ),
        )

    return {
        "guardado": True,
        "superado": superado_ahora,
        "tiene_medalla": ya_tenia or superado_ahora,
        "medalla_nueva": superado_ahora and not ya_tenia,
        "record": record,
    }


def puntos_totales():
    """Suma del mejor puntaje de cada nivel (repetir un nivel no infla el total)."""
    usuario = _usuario()
    if usuario is None:
        return 0
    fila = db.uno(
        "SELECT COALESCE(SUM(mejor_puntaje), 0) AS total FROM progreso WHERE usuario_id = ?",
        (usuario["id"],),
    )
    return fila["total"]


def total_medallas():
    usuario = _usuario()
    if usuario is None:
        return 0
    fila = db.uno(
        "SELECT COUNT(*) AS total FROM progreso WHERE usuario_id = ? AND superado = 1",
        (usuario["id"],),
    )
    return fila["total"]


def medallas_del_tema(fase, tema):
    usuario = _usuario()
    if usuario is None:
        return 0
    fila = db.uno(
        "SELECT COUNT(*) AS total FROM progreso "
        "WHERE usuario_id = ? AND fase = ? AND tema = ? AND superado = 1",
        (usuario["id"], fase, tema),
    )
    return fila["total"]