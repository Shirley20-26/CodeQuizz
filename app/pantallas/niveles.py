from kivy.factory import Factory
from kivy.metrics import dp, sp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex

from app import progreso
from app.catalogo import COLORES_MEDALLA, ESTILOS, FASES, tipo_medalla, total_niveles
from app.pantallas.base import MedallaIcono, PantallaConFondo

COLOR_BLOQUEADO = "#64748B"
SIN_MEDALLA = [0.35, 0.35, 0.45, 1]


class PantallaNiveles(PantallaConFondo):
    titulo = StringProperty("")
    fase = "colegio"
    tema = "general"

    def abrir(self, fase, tema):
        """Se llama antes de entrar a esta pantalla para decir qué niveles mostrar."""
        self.fase = fase
        self.tema = tema

    def on_pre_enter(self):
        self.aplicar_fase(self.fase)
        info_tema = FASES[self.fase]["temas"][self.tema]
        self.titulo = info_tema["nombre"] if self.fase == "universidad" else "Elige tu nivel"

        estilo = ESTILOS[self.fase]
        total = total_niveles(self.fase, self.tema)
        caja = self.ids.contenedor
        caja.clear_widgets()

        for nivel, nombre in info_tema["niveles"].items():
            estado = progreso.estado_nivel(self.fase, self.tema, nivel)
            abierto = progreso.nivel_desbloqueado(self.fase, self.tema, nivel)

            # Medalla: de color si ya se ganó, gris si no
            icono = MedallaIcono()
            icono.pos_hint = {"center_y": 0.5}
            if estado["superado"]:
                icono.color = list(COLORES_MEDALLA[tipo_medalla(nivel, total)])
            else:
                icono.color = list(SIN_MEDALLA)

            if not abierto:
                detalle = "Bloqueado: supera el nivel anterior"
            elif estado["superado"]:
                detalle = f"Mejor puntaje: {estado['mejor_puntaje']}"
            else:
                detalle = "¡A jugar!"

            boton = Factory.BotonSecundario()
            boton.size_hint_y = 1
            boton.font_size = sp(estilo["tam_opcion"])
            boton.text = f"Nivel {nivel}: {nombre}\n{detalle}"
            color = estilo["opciones"][(nivel - 1) % 4] if abierto else COLOR_BLOQUEADO
            boton.background_color = get_color_from_hex(color)
            boton.background_disabled_normal = ""
            boton.disabled = not abierto
            boton.bind(width=lambda b, w: setattr(b, "text_size", (w - dp(16), None)))
            boton.bind(on_release=lambda _b, n=nivel: self.jugar_nivel(n))

            fila = BoxLayout(
                size_hint_y=None, height=dp(estilo["alto_fila"]), spacing=dp(10)
            )
            fila.add_widget(icono)
            fila.add_widget(boton)
            caja.add_widget(fila)

    def jugar_nivel(self, nivel):
        quiz = self.manager.get_screen("quiz")
        if quiz.iniciar_nivel(self.fase, self.tema, nivel):
            self.manager.current = "quiz"

    def volver(self):
        self.manager.current = "temas" if self.fase == "universidad" else "menu"