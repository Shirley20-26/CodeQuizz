from kivy.properties import StringProperty

from app import auth, progreso
from app.catalogo import NOMBRES_FASE
from app.pantallas.base import PantallaConFondo


class PantallaMenu(PantallaConFondo):
    saludo = StringProperty("")
    etapa = StringProperty("")
    resumen = StringProperty("")

    def on_pre_enter(self):
        usuario = auth.usuario_actual()
        if usuario is None:
            return
        self.aplicar_fase(usuario["fase"])
        self.saludo = f"¡Hola, {usuario['usuario']}!"
        self.etapa = f"Etapa: {NOMBRES_FASE[usuario['fase']]}"
        self.resumen = (
            f"Puntos: {progreso.puntos_totales()}   "
            f"Medallas: {progreso.total_medallas()}"
        )

    def jugar(self):
        fase = auth.usuario_actual()["fase"]
        if fase == "universidad":
            # En universidad primero se elige de qué tema hablar
            self.manager.current = "temas"
        else:
            self.manager.get_screen("niveles").abrir(fase, "general")
            self.manager.current = "niveles"

    def cerrar_sesion(self):
        auth.cerrar_sesion()
        self.manager.current = "inicio"