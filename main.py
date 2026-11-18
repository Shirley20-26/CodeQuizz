import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivy.utils import platform
from kivy.properties import StringProperty,BooleanProperty,NumericProperty
from app import auth, db
from app.pantallas.inicio import PantallaInicio
from app.pantallas.login import PantallaLogin
from app.pantallas.menu import PantallaMenu
from app.pantallas.niveles import PantallaNiveles
from app.pantallas.quiz import PantallaQuiz
from app.pantallas.recuperar import PantallaRecuperar
from app.pantallas.registro import PantallaRegistro
from app.pantallas.resultado import PantallaResultado
from app.pantallas.temas import PantallaTemas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


if platform not in ("android", "ios"):
    Window.size = (360, 720)

ARCHIVOS_KV = (
    "estilos", "inicio", "quiz", "resultado",
    "registro", "login", "recuperar", "menu",
    "temas", "niveles",
)


class CodeQuizApp(App):
    title = "CodeQuiz"

    def build(self):
      
        db.iniciar(self.user_data_dir)
        print("Base de datos en:", db.ruta())

       
        for archivo in ARCHIVOS_KV:
            Builder.load_file(os.path.join(BASE_DIR, "kv", f"{archivo}.kv"))

      
        gestor = ScreenManager(transition=FadeTransition(duration=0.2))
        for pantalla in (
            PantallaInicio(), PantallaQuiz(), PantallaResultado(),
            PantallaRegistro(), PantallaLogin(), PantallaRecuperar(),
            PantallaMenu(), PantallaTemas(), PantallaNiveles(),
        ):
            gestor.add_widget(pantalla)

        if auth.restaurar_sesion():
            gestor.current = "menu"

        return gestor


if __name__ == "__main__":
    CodeQuizApp().run()