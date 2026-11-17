from kivy.properties import StringProperty,BooleanProperty,NumericProperty,ListProperty
from kivy.uix.screenmanager import Screen

from app import auth


class PantallaResultado(Screen):
    titulo = StringProperty("")
    detalle = StringProperty("")
    racha_texto = StringProperty("")
    invitacion = StringProperty("")
    es_invitado = BooleanProperty(True)
    hay_medalla = BooleanProperty(False)
    texto_medalla = StringProperty("")
    puntaje = NumericProperty(0)
    puntaje_maximo = NumericProperty(0)
    color_medalla = ListProperty([1,0.84,0,1])

    def mostrar(self, fase, tema, nivel, puntos, aciertos, total, mejor_racha, info=None):
        superado = aciertos >= 3
        self.titulo = "¡Nivel superado!" if superado else "¡Buen intento!"
        self.detalle = f"Aciertos: {aciertos} de {total}\nPuntos: {puntos}"
        self.racha_texto = f"¡Tienes una racha de {mejor_racha}!"
        self.puntaje = puntos
        self.puntaje_maximo = total

        if superado:
            self.color_medalla = [1,0.84,0,1]
        else:
            self.color_medalla = [0.7,0.7,0.7,1]

        self.es_invitado = auth.usuario_actual() is None
        if self.es_invitado:
            self.invitacion = "Regístrate para guardar tu progreso"
        else:
            self.invitacion = "El guardado de puntos y medallas llega en la Fase 3"

    def ir_a_registro(self):
        self.manager.current = "registro"

    def jugar_otra_vez(self):
        self.manager.get_screen("quiz").iniciar_nivel(1)
        self.manager.current = "quiz"

    def volver(self):
        self.manager.current = "menu" if auth.usuario_actual() else "inicio"