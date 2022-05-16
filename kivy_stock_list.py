from kivy.app import App
from kivy.uix.gridlayout import GridLayout


# Name vor 'App' wird als Fenster Titel benutzt
class MyApp(App):
    # Baut das initiale Fenster auf
    def build(self):
        self.window = GridLayout()
        # Widgets zum Layout hinzufügen

        return self.window


# Standard - sollte immer genutzt werden
if __name__ == '__main__':
    # Instanz der App erzeugen
    app = MyApp()
    # App starten
    app.run()
