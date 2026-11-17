# Aquí vive todo lo que describe el "mapa" del juego: etapas, temas, niveles,
# medallas y el aspecto de cada etapa. Si quieres agregar un tema o un nivel,
# se hace aquí (y se agregan sus preguntas en preguntas.json).

PREGUNTAS_POR_NIVEL = 5   # máximo de preguntas por partida
PUNTOS_BASE = 10          # puntos por acierto; se multiplica por el número de nivel

NOMBRES_FASE = {
    "escuela": "Escuela",
    "colegio": "Colegio",
    "universidad": "Universidad",
}

FASES = {
    "escuela": {
        "temas": {
            "general": {
                "nombre": "Hardware y software",
                "niveles": {
                    1: "Conoce tu computadora",
                    2: "Programas y apps",
                    3: "Hardware y software juntos",
                },
            }
        }
    },
    "colegio": {
        "temas": {
            "general": {
                "nombre": "Informática",
                "niveles": {
                    1: "Hardware",
                    2: "Software y sistemas operativos",
                    3: "Programación básica",
                },
            }
        }
    },
}

# Temas de universidad (claves iguales a las de preguntas.json)
_TEMAS_UNIVERSIDAD = (
    ("programacion", "Programación"),
    ("redes", "Redes e internet"),
    ("bases_datos", "Bases de datos"),
    ("seguridad", "Seguridad informática"),
    ("ia", "Inteligencia artificial"),
    ("hardware", "Hardware"),
)
_NIVELES_UNIVERSIDAD = {1: "Básico", 2: "Intermedio"}

FASES["universidad"] = {
    "temas": {
        clave: {"nombre": nombre, "niveles": _NIVELES_UNIVERSIDAD}
        for clave, nombre in _TEMAS_UNIVERSIDAD
    }
}

# Aspecto de cada etapa. "invitado" usa el mismo estilo que colegio.
ESTILOS = {
    "escuela": {
        "fondo": "#0369A1",
        "opciones": ["#F97316", "#DB2777", "#7C3AED", "#CA8A04"],  # sin verde ni rojo
        "tam_pregunta": 24,
        "tam_opcion": 20,
        "alto_opcion": 64,
        "alto_fila": 84,
    },
    "colegio": {
        "fondo": "#1E1B4B",
        "opciones": ["#4338CA"] * 4,
        "tam_pregunta": 21,
        "tam_opcion": 16,
        "alto_opcion": 58,
        "alto_fila": 68,
    },
    "universidad": {
        "fondo": "#0F172A",
        "opciones": ["#334155"] * 4,
        "tam_pregunta": 20,
        "tam_opcion": 16,
        "alto_opcion": 56,
        "alto_fila": 64,
    },
}
ESTILOS["invitado"] = ESTILOS["colegio"]

COLORES_MEDALLA = {
    "bronce": (0.80, 0.50, 0.20, 1),
    "plata": (0.75, 0.77, 0.82, 1),
    "oro": (1.0, 0.84, 0.0, 1),
}
NOMBRES_MEDALLA = {"bronce": "Bronce", "plata": "Plata", "oro": "Oro"}


def existe_nivel(fase, tema, nivel):
    return nivel in FASES.get(fase, {}).get("temas", {}).get(tema, {}).get("niveles", {})


def total_niveles(fase, tema):
    return len(FASES[fase]["temas"][tema]["niveles"])


def minimo_aprobar(total):
    """Aciertos necesarios: el 60 % redondeado hacia arriba (3 de 5, 3 de 4)."""
    return (total * 3 + 4) // 5


def aprobado(aciertos, total):
    return total > 0 and aciertos >= minimo_aprobar(total)


def tipo_medalla(nivel, total):
    """El último nivel siempre da oro; el primero, bronce; los del medio, plata."""
    if nivel == total:
        return "oro"
    if nivel == 1:
        return "bronce"
    return "plata"