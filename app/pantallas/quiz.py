from kivy.properties import NumericProperty, StringProperty
from kivy.utils import get_color_from_hex

from app import auth, progreso
from app.catalogo import ESTILOS, PREGUNTAS_POR_NIVEL, PUNTOS_BASE
from app.pantallas.base import PantallaConFondo
from app.preguntas import obtener_preguntas, ruta_imagen

COLOR_BIEN = get_color_from_hex("#16A34A")
COLOR_MAL = get_color_from_hex("#DC2626")


class PantallaQuiz(PantallaConFondo):
    texto_progreso = StringProperty("")
    pregunta_texto = StringProperty("")
    mensaje = StringProperty("")
    imagen = StringProperty("")
    puntos = NumericProperty(0)
    racha = NumericProperty(0)
    tam_pregunta = NumericProperty(21)
    tam_opcion = NumericProperty(16)
    alto_opcion = NumericProperty(58)

    def iniciar_nivel(self, fase, tema, nivel):
        """Arranca una partida. Devuelve True si pudo, False si no está permitido."""
        if not progreso.puede_jugar(fase, tema, nivel):
            return False
        preguntas = obtener_preguntas(fase, tema, nivel, PREGUNTAS_POR_NIVEL)
        if not preguntas:
            return False

        # Aspecto según la etapa
        estilo = ESTILOS.get(fase, ESTILOS["colegio"])
        self.aplicar_fase(fase)
        self.colores_opcion = [get_color_from_hex(c) for c in estilo["opciones"]]
        self.tam_pregunta = estilo["tam_pregunta"]
        self.tam_opcion = estilo["tam_opcion"]
        self.alto_opcion = estilo["alto_opcion"]

        # Estado de la partida
        self.fase, self.tema, self.nivel = fase, tema, nivel
        self.preguntas = preguntas
        self.indice = 0
        self.aciertos = 0
        self.mejor_racha = 0
        self.puntos = 0
        self.racha = 0
        self.bloqueado = False
        self.mostrar_pregunta()
        return True

    def mostrar_pregunta(self):
        pregunta = self.preguntas[self.indice]
        self.texto_progreso = f"Pregunta {self.indice + 1} de {len(self.preguntas)}"
        self.pregunta_texto = pregunta["pregunta"]
        self.imagen = ruta_imagen(pregunta.get("imagen", ""))
        self.mensaje = ""
        self.bloqueado = False

        for i in range(4):
            boton = self.ids[f"op{i}"]
            boton.text = pregunta["opciones"][i]
            boton.background_color = self.colores_opcion[i]

        self.ids.btn_siguiente.opacity = 0
        self.ids.btn_siguiente.disabled = True

    def responder(self, elegida):
        if self.bloqueado:  # evita contestar dos veces la misma pregunta
            return
        self.bloqueado = True

        pregunta = self.preguntas[self.indice]
        correcta = pregunta["correcta"]

        if elegida == correcta:
            self.aciertos += 1
            self.racha += 1
            self.puntos += PUNTOS_BASE * self.nivel  # niveles más difíciles dan más puntos
            self.mejor_racha = max(self.mejor_racha, self.racha)
            self.mensaje = "[b]¡Correcto![/b]\n" + pregunta["explicacion"]
        else:
            self.racha = 0
            self.ids[f"op{elegida}"].background_color = COLOR_MAL
            self.mensaje = "[b]Casi...[/b]\n" + pregunta["explicacion"]

        self.ids[f"op{correcta}"].background_color = COLOR_BIEN

        es_ultima = self.indice + 1 >= len(self.preguntas)
        self.ids.btn_siguiente.text = "Ver resultado" if es_ultima else "Siguiente"
        self.ids.btn_siguiente.opacity = 1
        self.ids.btn_siguiente.disabled = False

    def siguiente(self):
        if self.indice + 1 < len(self.preguntas):
            self.indice += 1
            self.mostrar_pregunta()
            return

        total = len(self.preguntas)
        info = progreso.guardar_resultado(
            self.fase, self.tema, self.nivel, self.puntos, self.aciertos, total
        )
        resultado = self.manager.get_screen("resultado")
        resultado.mostrar(
            self.fase, self.tema, self.nivel,
            self.puntos, self.aciertos, total, self.mejor_racha, info,
        )
        self.manager.current = "resultado"

    def salir(self):
        # Con sesión vuelve a la lista de niveles; el invitado, al inicio.
        self.manager.current = "niveles" if auth.usuario_actual() else "inicio"