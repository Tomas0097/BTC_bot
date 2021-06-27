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
    frequency_of_purchase_in_seconds = 10

    income = 0
    last_bought_position = None
    bought_positions = []

    def __init__(self, currency_for_trading):
        self.currency_for_trading = currency_for_trading

    def run_trading_session1(self):
        print(f"Bot started trading currency: {self.currency_for_trading}\n")

        while True:
            time.sleep(self.frequency_of_purchase_in_seconds)

            current_bought_position = self.get_currency_price()

            selled_profitable_positions = []

            # Check income state
            for position in self.bought_positions:
                self.income += (current_bought_position - position)

                # Remove selled profitable positions
                if position < current_bought_position:
                    self.bought_positions.remove(position)
                    selled_profitable_positions.append(position)


            self.last_bought_position = current_bought_position
            self.bought_positions.append(current_bought_position)

            # Get current time
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)

            print(f"{current_time} - New bought position - {current_bought_position}")
            print(f"{len(self.bought_positions)} Own positions: {self.bought_positions}")
            print(f"Selled positions: {selled_profitable_positions if selled_profitable_positions else 'none'}")
            print(f"Income: {self.income}\n")

    # def run_trading_session2(self):
    #     print(f"Bot started trading currency: {self.currency_for_trading}")
    #
    #     while True:
    #         time.sleep(self.frequency_of_purchase_in_seconds)
    #
    #         current_bought_position = self.get_currency_price()
    #
    #         if not self.bought_positions or (current_bought_position < self.last_bought_position):
    #
    #             self.last_bought_position = current_bought_position
    #             self.bought_positions.append(current_bought_position)
    #
    #             t = time.localtime()
    #             current_time = time.strftime("%H:%M:%S", t)
    #
    #             print(f"{current_time} - Bought position - {current_bought_position}")
    #             print(f"Bought positions - {self.bought_positions}\n")

    def get_currency_price(self):
        binance_client = BinanceClient(self.currency_for_trading)
        return binance_client.get_currency_price()

bot = Bot("BTCUSDT")
bot.run_trading_session1()
