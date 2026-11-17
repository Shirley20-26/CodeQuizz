import json
import os
import random

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_PREGUNTAS = os.path.join(BASE, "data", "preguntas.json")
RUTA_IMAGENES = os.path.join(BASE, "assets", "img")

_cache = None


def cargar_todas():
    """Lee el JSON una sola vez y lo guarda en memoria."""
    global _cache
    if _cache is None:
        with open(RUTA_PREGUNTAS, "r", encoding="utf-8") as archivo:
            _cache = json.load(archivo)["preguntas"]
    return _cache


def ruta_imagen(nombre):
    """Ruta del dibujito de una pregunta, o '' si no hay imagen o no existe."""
    if not nombre:
        return ""
    ruta = os.path.join(RUTA_IMAGENES, os.path.basename(nombre))  # basename: sin rutas raras
    return ruta if os.path.exists(ruta) else ""


def obtener_preguntas(fase, tema, nivel, cantidad=5):
    """Devuelve hasta 'cantidad' preguntas al azar de ese nivel,
    con las opciones mezcladas (la respuesta correcta cambia de lugar)."""
    candidatas = [
        p for p in cargar_todas()
        if p["fase"] == fase and p["tema"] == tema and p["nivel"] == nivel
    ]
    random.shuffle(candidatas)

    elegidas = []
    for pregunta in candidatas[:cantidad]:
        copia = dict(pregunta)
        opciones = list(pregunta["opciones"])
        texto_correcto = opciones[pregunta["correcta"]]
        random.shuffle(opciones)
        copia["opciones"] = opciones
        copia["correcta"] = opciones.index(texto_correcto)
        elegidas.append(copia)
    return elegidas