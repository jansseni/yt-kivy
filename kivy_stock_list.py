from threading import Thread

import yfinance as yfinance
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


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
        Clock.schedule_once(self.switch_to_next_view, 2)

    def switch_to_next_view(self, *args):
        app.screen_manager.current = 'stockView'


class StockView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (0.9, 0.9)
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
        # Label für Nachrichten einfügen
        self.message = Label(size_hint=(1, 0.1))
        self.add_widget(self.message)
        # second row
        self.stock_view = ScrollView(size_hint=(1, None),
                                     size=(Window.width, Window.height * 0.8),
                                     do_scroll_x=False,
                                     do_scroll_y=True)
        self.stock_list = GridLayout(cols=4,
                                     size_hint=(1, None),
                                     height=self.minimum_height,
                                     row_default_height=30,
                                     row_force_default=True)
        self.stock_view.add_widget(self.stock_list)
        self.add_widget(self.stock_view)
        # third row
        self.stock_add = GridLayout(cols=3, size_hint=(1, 0.15))
        self.add_widget(self.stock_add)
        self.ticker_text = Label(text='Symbol/Ticker:',
                                 size_hint_x=0.2,
                                 height=Window.height * 0.1)
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
        # wir fragen eine externe API ab
        # Daher ist es nicht schlecht den Benutzer zu informieren, dass etwas
        # im Hintergrund passiert
        self.message.text = 'Bitte warten, während die Daten abgefragt werden...'
        query_data_thread = Thread(target=self.query_stock_data)
        query_data_thread.start()

    def query_stock_data(self):
        # Jetzt müssen wir die richtigen Daten für den eingegebenen Ticker
        # noch von Yahoo Finance abfragen
        symbol = self.ticker_input.text.strip()
        stock = yfinance.Ticker(ticker=symbol)
        # Davon interessiert uns nur das info Objekt
        data = stock.info
        if 'regularMarketPrice' in data and data.get('regularMarketPrice') is not None:
            # aus dem Info Objekt können wir uns jetzt die Daten zusammen bauen
            # msf.de
            price = f'{data.get("regularMarketPrice"):.2f} {data.get("currency")}'
            self.add_ticker_row(data.get('symbol'), data.get('longName'), price)
        else:
            # Fehlermeldung, falls kein Preis gefunden werden konnte
            self.message.text = f'Für das angegebene Symbol {symbol} gab es kein Ergebnis.'

    def add_ticker_row(self, ticker, name, price):
        # Die Daten sind geladen - wir können die Nachricht entfernen
        self.message.text = ''
        ticker = Label(text=ticker, size_hint_x=0.2)
        self.stock_list.add_widget(ticker)
        name = Label(text=name, size_hint_x=0.4)
        self.stock_list.add_widget(name)
        price = Label(text=price, size_hint_x=0.2)
        self.stock_list.add_widget(price)
        delete = Button(text='Entfernen', size_hint_x=0.2)
        delete.bind(on_press=self.remove_ticker_row)
        self.stock_list.add_widget(delete)

    def remove_ticker_row(self, *args):
        print('Aktien entfernen')


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.welcome_view = WelcomeView()
        screen = Screen(name='welcomeView')
        screen.add_widget(self.welcome_view)
        self.screen_manager.add_widget(screen)

        self.stock_view = StockView()
        screen = Screen(name='stockView')
        screen.add_widget(self.stock_view)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    app = MyApp()
    app.run()
