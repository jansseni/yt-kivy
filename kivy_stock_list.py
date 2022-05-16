from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MyApp(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        # Wir wollen nicht die gesamte Größe ausnutzen.
        # Damit würde alles am Rand kleben und nicht schön aussehen.
        # Also nehmen wir nur 60% der Breite (0.6x) und
        # 70% der Höhe (0.7y)
        self.window.size_hint = (0.6, 0.7)
        # Damit es jetzt aber nicht links oben klebt
        # müssen wir den Inhalt noch zentrieren.
        # Die x Position des Inhalts soll also bei 0.5
        # der Fensterbreite und 0.5 der Fensterhöhe liegen.
        self.window.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.window.add_widget(Image(source='logo_weiß.png'))
        # Schriftgröße und Farbe anpassen
        self.greeting = Label(text='Wie heißt du?', font_size=52, color='#33cccc')
        self.window.add_widget(self.greeting)
        # padding_y passt den Abstand von Text zu Box-Rand an
        # size_hint setzt wieder die Größe des Elements
        # Wir wollen einen Abstand über und unter dem Text von je 20 px
        # Das Eingabefeld selbst soll weiter die volle Breite haben,
        # aber nur die halbe Höhe
        self.user = TextInput(multiline=False, size_hint=(1, 0.5), padding_y=(40, 40))
        self.window.add_widget(self.user)
        # Button soll die gleiche Größe bekommen wie das Eingabefeld.
        # Außerdem soll der Text im Fettdruck dargestellt werden
        # Und schlussendlich noch die Hintergrundfarbe anpassen
        # Ohne background_normal wird die Hintergrundfarbe dunkler angezeigt
        self.entrance_button = Button(text='Eintreten', size_hint=(1, 0.5), bold=True, background_color='#33cccc', background_normal='')
        self.entrance_button.bind(on_press=self.entrance_button_behaviour)
        self.window.add_widget(self.entrance_button)

        return self.window

    def entrance_button_behaviour(self, *args):
        self.greeting.text = f'Herzlich Willkommen {self.user.text}.'


if __name__ == '__main__':
    app = MyApp()
    app.run()
