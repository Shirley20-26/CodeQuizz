from kivy.uix.screenmanager import Screen

from app import auth, ventanas

CAMPOS = ("in_usuario", "in_correo", "in_dia", "in_mes", "in_anio", "in_clave", "in_clave2")


class PantallaRegistro(Screen):

    def on_pre_enter(self):
        self.limpiar()

    def limpiar(self):
        for campo in CAMPOS:
            self.ids[campo].text = ""
        self.ids.lbl_error.text = ""

    def crear_cuenta(self):
        ok, resultado = auth.registrar(
            self.ids.in_usuario.text,
            self.ids.in_correo.text,
            self.ids.in_dia.text,
            self.ids.in_mes.text,
            self.ids.in_anio.text,
            self.ids.in_clave.text,
            self.ids.in_clave2.text,
        )
        if not ok:
            self.ids.lbl_error.text = resultado
            return

        self.limpiar()  # borra la contraseña de la pantalla
        ventanas.mostrar_codigo(
            titulo="¡Cuenta creada!",
            mensaje="Guarda este código en un lugar seguro.\n"
                    "Lo necesitarás si olvidas tu contraseña.",
            codigo=resultado,
            al_cerrar=lambda: setattr(self.manager, "current", "menu"),
        )

    def volver(self):
        self.manager.current = "inicio"