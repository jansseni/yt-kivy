from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


# ausgelagert in eigene Klasse die von GridLayout erbt
class WelcomeView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        self.add_widget(Image(source='logo_weiß.png'))
        self.greeting = Label(text='Wie heißt du?',
                              font_size=18,
                              color='#33cccc')
        self.add_widget(self.greeting)
        self.user = TextInput(multiline=False,
                              padding_y=(20, 20),
                              size_hint=(1, 0.5)
                              )
        self.add_widget(self.user)
        self.entrance_button = Button(text='Eintreten',
                                      size_hint=(1, 0.5),
                                      bold=True,
                                      background_color='#33cccc',
                                      background_normal='')
        self.entrance_button.bind(on_press=self.entrance_button_behaviour)
        self.add_widget(self.entrance_button)

    def entrance_button_behaviour(self, *args):
        self.greeting.text = f'Herzlich Willkommen {self.user.text}.'
        # Clock lässt Dinge geplant ausführen
        # Übergeben wird, was ausgeführt werden soll und wann - von jetzt ab in Sekunden
        # Wir wollen die Willkommen Nachricht 2 Sekunden anzeigen
        # und dann in den nächsten View wechseln
        Clock.schedule_once(self.switch_to_next_view, 2)

    # Funktion, um im ScreenManager den nächsten View zu setzen
    def switch_to_next_view(self, *args):
        app.screen_manager.current = 'stockView'


# Der neue View um die Aktien anzuzeigen
class StockView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        # Dieser View soll etwas größer sein
        self.size_hint = (0.9, 0.9)
        # Aber auch wieder zentriert
        self.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }
        '''
        Ticker      Name        Preis       Löschen
        Ticker      Name        Preis       Löschen
        ------------------------------------------
        Label   Tickereingabe               Zufügen
        '''
        # Wenn die Liste der Aktien länger wird, muss sie scrollbar sein
        # Deswegen ein ScrollView für den oberen Teil
        # Der View soll die volle Breite einnehmen - das sind 90% der Bildschirmbreite
        # Aber nur 90% der Höhe, damit wir noch Platz für die ander Komponente haben
        self.stock_view = ScrollView(size_hint=(1, 0.9))
        # In dem Bereich soll alles in 4 Spalten unterteilt sein
        # Also brauchen wir ein GridLayout mit 4 Spalten
        self.stock_list = GridLayout(cols=4)
        # Das muss dann erstmal an den ScrollView gefügt werden
        self.stock_view.add_widget(self.stock_list)
        # Und der ScrollView wiederum an unseren Haupt-View
        self.add_widget(self.stock_view)
        # Die Eingabe einer neuen Aktie ist in 3 Spalten dargestellt
        # Also auch wieder ein GridLayout mit 3 Spalten
        # Auch hier nehmen wir die gesamte Breite - 90% vom Bildschirm
        # Aber nur 10% der Höhe
        self.stock_add = GridLayout(cols=3, size_hint=(1, 0.1))
        # Und der Bereich muss natürlich auch dem View wieder zugefügt werden
        self.add_widget(self.stock_add)
        # In das Layout kommen jetzt ein Label, ein Eingabefeld und ein Button
        self.ticker_text = Label(text='Symbol/Ticker:',
                                 size_hint=(0.2, 0.5))
        self.stock_add.add_widget(self.ticker_text)
        self.ticker_input = TextInput(multiline=False,
                                      padding_y=(10, 10),
                                      size_hint=(0.6, 0.5)
                                      )
        self.stock_add.add_widget(self.ticker_input)
        self.ticker_add = Button(text='Zufügen',
                                      size_hint=(0.2, 0.5),
                                      bold=True,
                                      background_color='#33cccc',
                                      background_normal='')
        self.ticker_add.bind(on_press=self.add_ticker_symbol)
        self.stock_add.add_widget(self.ticker_add)

    def add_ticker_symbol(self, *args):
        print('Test für das zufügen von Aktien')


class MyApp(App):
    def build(self):
        # ScreenManager übernimmt die Arbeit welcher View angezeigt werden soll
        self.screen_manager = ScreenManager()
        # Die Willkommen Seite wird erzeugt, aber noch nicht angezeigt
        self.welcome_view = WelcomeView()
        # Setzt einen Namen, um später einfacher auf die Seiten referenzieren zu können
        screen = Screen(name='welcomeView')
        # Der Name bekommt die Seite zugeordnet, die unter dem Namen erreichbar sein soll
        screen.add_widget(self.welcome_view)
        # Und der so erzeugte Screen wird dem ScreenManager übergeben
        # Dieser weiß damit welche Seite mit welchem Namen in Verbindung steht
        # Jede Seite wird so dem ScreenManager zugefügt
        self.screen_manager.add_widget(screen)

        # Jetzt muss der neue View noch dem ScreenManager bekannt gemacht werden
        # Sonst können wir das natürlich nicht aufrufen
        self.stock_view = StockView()
        screen = Screen(name='stockView')
        screen.add_widget(self.stock_view)
        self.screen_manager.add_widget(screen)

        # ScreenManager zurückgeben, um die Views verfügbar zu machen
        return self.screen_manager


if __name__ == '__main__':
    app = MyApp()
    app.run()
