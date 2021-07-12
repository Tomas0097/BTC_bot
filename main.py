import copy
import time
from binance import Client, ThreadedWebsocketManager


class BinanceClient:
    API_KEY = "lbhqUY1k95VIH2x0ahLLD78M40j4v9nUjJoYxaXCekpm80Xsenb9ujUO5IpryOOQ"
    API_SECRET = "nxUn2pKY4p1P1Z84hgveal2ZAkmf6OR9M4K5Oo0J7gv6HJjFWLbCoG1o4JmSyX5q"

    def __init__(self, currency_symbol):
        # Currency symbol is for Binance pair of currencies. For working with BTC is required symbol: 'BTCUSDT'.
        # 'BTCUSDT' is pair between BTC and USDT. USDT is a cryptocurrency that is backed 1-to-1 with dollar.
        self.currency_symbol = currency_symbol

        # Connect to binance web socket
        self.binance_web_socket = ThreadedWebsocketManager(api_key=self.API_KEY, api_secret=self.API_SECRET)
        self.binance_web_socket.start()

        # Set up connection with binance API
        self.client = Client(self.API_KEY, self.API_SECRET)

    def get_currency_price(self):
        return float(self.client.get_avg_price(symbol=self.currency_symbol)["price"])

    def get_currency_price_real_time(self):
        self.binance_web_socket.start_trade_socket(callback=self.handle_socket_message, symbol=self.currency_symbol)

    @staticmethod
    def handle_socket_message(msg):
        print(f"BTC price in USDT: {msg['p']}")


class Bot:
    frequency_of_purchase_in_seconds = 5

    income = 0

    last_but_one_position = None
    last_position = None
    current_position = None
    bought_current_position = None
    selled_profitable_positions = []
    own_positions = []

    def __init__(self, currency_for_trading):
        self.currency_for_trading = currency_for_trading

    def run_trading_session1(self):
        print(f"Bot started trading currency: {self.currency_for_trading}\n")

        while True:
            time.sleep(self.frequency_of_purchase_in_seconds)

            # Set up current position, last but one position and last position.
            self.set_up_positions()

            if self.rules_met_to_buy():
                self.buy_position(self.current_position)

            selling_positions = []

            # Check income state
            for position in self.own_positions[:-1]:
                self.income += (self.current_position - position)

                # Sell profitable positions
                if position < self.current_position:
                    self.sell_position(position)
                    selling_positions.append(position)

            print(f"{self.get_current_time()} - Current price: {self.current_position} - Bought: {'YES' if self.bought_current_position else 'NO'}")
            print(f"Selling positions: {selling_positions if selling_positions else 'none'}")
            print(f"All selled positions: {self.selled_profitable_positions if self.selled_profitable_positions else 'none'}")
            print(f"{len(self.own_positions)} Own positions: {self.own_positions}")
            print(f"Income: {self.income}\n")

    def rules_met_to_buy(self):
        if not self.last_but_one_position or not self.last_position:
            return False

        if self.last_position < self.current_position:
            return False

        if (self.last_but_one_position > self.last_position) and (self.last_position > self.current_position):
            return False

        return True

    def buy_position(self, position):
        self.bought_current_position = position
        self.own_positions.append(position)

    def sell_position(self, position):
        self.own_positions.remove(position)
        self.selled_profitable_positions.append(position)

    def set_up_positions(self):
        self.last_but_one_position = copy.deepcopy(self.last_position)
        self.last_position = copy.deepcopy(self.current_position)
        self.current_position = self.get_currency_price()

    def get_currency_price(self):
        return BinanceClient(self.currency_for_trading).get_currency_price()

    @staticmethod
    def get_current_time():
        return time.strftime("%H:%M:%S", time.localtime())


bot = Bot("BTCUSDT")
bot.run_trading_session1()
