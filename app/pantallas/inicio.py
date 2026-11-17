from kivy.uix.screenmanager import Screen


class PantallaInicio(Screen):

    def jugar_como_invitado(self):
        """El invitado juega una demo corta, sin registrarse ni guardar nada."""
        quiz = self.manager.get_screen("quiz")
        if quiz.iniciar_nivel("invitado", "demo", 1):
            self.manager.current = "quiz"

    def ir_a_login(self):
        self.manager.current = "login"