from kivy.factory import Factory
from kivy.metrics import dp

from app import progreso
from app.catalogo import FASES
from app.pantallas.base import PantallaConFondo


class PantallaTemas(PantallaConFondo):

    def on_pre_enter(self):
        self.aplicar_fase("universidad")
        caja = self.ids.contenedor
        caja.clear_widgets()

        for clave, tema in FASES["universidad"]["temas"].items():
            ganadas = progreso.medallas_del_tema("universidad", clave)
            total = len(tema["niveles"])

            boton = Factory.BotonSecundario()
            boton.height = dp(64)
            boton.text = f"{tema['nombre']}\n{ganadas} de {total} medallas"
            boton.bind(on_release=lambda _b, c=clave: self.elegir(c))
            caja.add_widget(boton)

    def elegir(self, clave):
        self.manager.get_screen("niveles").abrir("universidad", clave)
        self.manager.current = "niveles"

    def volver(self):
        self.manager.current = "menu"