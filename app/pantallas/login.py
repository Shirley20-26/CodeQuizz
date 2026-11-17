from kivy.uix.screenmanager import Screen

from app import auth


class PantallaLogin(Screen):

    def on_pre_enter(self):
        self.ids.in_usuario.text = ""
        self.ids.in_clave.text = ""
        self.ids.lbl_error.text = ""

    def entrar(self):
        ok, mensaje = auth.iniciar_sesion(
            self.ids.in_usuario.text, self.ids.in_clave.text
        )
        self.ids.in_clave.text = ""  # nunca dejamos la contraseña en pantalla
        if ok:
            self.manager.current = "menu"
        else:
            self.ids.lbl_error.text = mensaje

    def ir_a_recuperar(self):
        self.manager.current = "recuperar"

    def ir_a_registro(self):
        self.manager.current = "registro"

    def volver(self):
        self.manager.current = "inicio"