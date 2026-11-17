from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty,BooleanProperty,NumericProperty

def _etiqueta(texto, tamano, **extra):
    lbl = Label(
        text=texto,
        font_size=tamano,
        halign="center",
        valign="middle",
        markup=True,
        **extra,
    )
    lbl.bind(size=lambda l, s: setattr(l, "text_size", s))
    return lbl


def mostrar_codigo(titulo, mensaje, codigo, al_cerrar):
    """Ventana emergente que muestra el código de recuperación."""
    contenido = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
    contenido.add_widget(_etiqueta(mensaje, "15sp"))
    contenido.add_widget(
        _etiqueta(f"[b]{codigo}[/b]", "28sp", color=(0.98, 0.8, 0.08, 1))
    )

    boton = Button(text="Ya lo guardé", size_hint_y=None, height=dp(50))
    contenido.add_widget(boton)

    ventana = Popup(
        title=titulo,
        content=contenido,
        size_hint=(0.92, 0.6),
        auto_dismiss=False,  # no se cierra tocando afuera
    )

    def cerrar(*_):
        ventana.dismiss()
        al_cerrar()

    boton.bind(on_release=cerrar)
    ventana.open()