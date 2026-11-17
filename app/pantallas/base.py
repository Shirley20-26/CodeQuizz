from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

from app.catalogo import ESTILOS


class PantallaConFondo(Screen):
    """Pantalla base: el color de fondo cambia según la etapa del estudiante."""
    color_fondo = ListProperty(get_color_from_hex("#1E1B4B"))

    def aplicar_fase(self, fase):
        estilo = ESTILOS.get(fase, ESTILOS["colegio"])
        self.color_fondo = get_color_from_hex(estilo["fondo"])


class MedallaIcono(Widget):
    """Círculo de color. Su diseño está en estilos.kv."""
    color = ListProperty([0.35, 0.35, 0.45, 1])