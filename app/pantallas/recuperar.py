from kivy.uix.screenmanager import Screen

from app import auth, ventanas

CAMPOS = ("in_usuario", "in_codigo", "in_clave", "in_clave2")


class PantallaRecuperar(Screen):

    def on_pre_enter(self):
        self.limpiar()

    def limpiar(self):
        for campo in CAMPOS:
            self.ids[campo].text = ""
        self.ids.lbl_error.text = ""

    def cambiar(self):
        ok, resultado = auth.recuperar_clave(
            self.ids.in_usuario.text,
            self.ids.in_codigo.text,
            self.ids.in_clave.text,
            self.ids.in_clave2.text,
        )
        if not ok:
            self.ids.lbl_error.text = resultado
            return

        self.limpiar()
        ventanas.mostrar_codigo(
            titulo="Contraseña cambiada",
            mensaje="Tu código anterior ya no sirve.\nGuarda este código nuevo:",
            codigo=resultado,
            al_cerrar=lambda: setattr(self.manager, "current", "login"),
        )

    def volver(self):
        self.manager.current = "login"