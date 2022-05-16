from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MyApp(App):
    def build(self):
        self.window = GridLayout()
        # Setzt das Layout auf eine Spalte - also gesamte Breite
        self.window.cols = 1
        # Bild hinzufügen - source ist der PFad zur Datei
        self.window.add_widget(Image(source='logo_weiß.png'))
        # Ausgabetext erzeugen
        self.greeting = Label(text='Wie heißt du?')
        # Ausgabetext zum Layout hinzufügen
        self.window.add_widget(self.greeting)
        # Eingabe vom Benutzer erfragen
        # multiline=False weil wir nur eine Zeile wollen
        self.user = TextInput(multiline=False)
        # Eingabeabfrage zum Layout hinzufügen
        self.window.add_widget(self.user)
        # Absenden Button erzeugen
        self.entrance_button = Button(text='Eintreten')
        # callback an den Button hinzufügen
        # Ein callback ist nur eine Referenz auf eine Funktion die
        # aufgerufen werden soll. Deshalb keine Funktionsklammern '()'
        self.entrance_button.bind(on_press=self.entrance_button_behaviour)
        # Button hinzufügen
        self.window.add_widget(self.entrance_button)

        return self.window

    # bei einem 'callback' - also einer Funktion die durch Klick
    # des Buttons aufgerufen wird, werden mehrere Werte übergeben
    # Wir interessieren aktuell nicht dafür, deswegen werden sie
    # einfach in *args gesammelt
    def entrance_button_behaviour(self, *args):
        # Label ändern, um den Benutzer zu begrüßen
        # Dafür nehmen wir den Text aus dem self.user Feld.
        # Das ist was der Benutzer eingegeben hat
        self.greeting.text = f'Herzlich Willkommen {self.user.text}.'


if __name__ == '__main__':
    app = MyApp()
    app.run()
