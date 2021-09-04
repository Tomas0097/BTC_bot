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

    def get_historical_trades(self):
        self.client.get_historical_trades(symbol=self.currency_symbol)

    @staticmethod
    def handle_socket_message(msg):
        print(f"BTC price in USDT: {msg['p']}")


class Bot:
    number_of_actions = 40
    frequency_of_purchase_in_seconds = 3

    income_of_selled_positions = 0

    last_but_one_position = None
    last_position = None
    current_position = None
    selled_profitable_positions = []
    own_positions = []

    def __init__(self, currency_for_trading):
        self.currency_for_trading = currency_for_trading

    def run_trading_session(self):
        print(f"\nBot started trading currency: {self.currency_for_trading}\n")

        while self.number_of_actions:
            self.number_of_actions -= 1
            time.sleep(self.frequency_of_purchase_in_seconds)

            # Set up current position, last but one position and last position.
            self.set_up_positions()

            bought_current_position = self.buy_position(self.current_position) if self.rules_met_to_buy() else None

            selling_positions = [position for position in self.own_positions if position < self.current_position]

            for position in selling_positions:
                self.sell_position(position)

            self.display_info(bought_current_position, selling_positions)

    def rules_met_to_buy(self):
        if not self.last_but_one_position or not self.last_position:
            return False

        if self.last_position < self.current_position:
            return False

        if (self.last_but_one_position > self.last_position) and (self.last_position > self.current_position):
            return False

        return True

    def buy_position(self, position):
        self.own_positions.append(position)
        return position

    def sell_position(self, position):
        self.selled_profitable_positions.append(position)
        self.income_of_selled_positions += (self.current_position - position)
        self.own_positions.remove(position)

    def set_up_positions(self):
        self.last_but_one_position = copy.deepcopy(self.last_position)
        self.last_position = copy.deepcopy(self.current_position)
        self.current_position = self.get_currency_price()

    def get_income_of_owned_positions(self):
        income_from_owned_positions = sum([(self.current_position - position) for position in self.own_positions])

        return income_from_owned_positions if income_from_owned_positions else 0

    # TODO: Income is in general price difference for now, but it is needed in percentage difference. Formula can be found here:
    #       https://www.justfreetools.com/cs/kalkulacky/matematicke-kalkulacky/percentage-increase-decrease-calculator
    def display_info(self, bought_current_position, selling_positions):
        income_of_owned_positions = self.get_income_of_owned_positions()
        total_income = self.income_of_selled_positions + income_of_owned_positions

        print(f"{self.get_current_time()} - Current price: {self.current_position} - Bought: {'YES' if bought_current_position else 'NO'}")
        print(f"Selling positions: {selling_positions if selling_positions else 'none'}")
        print(f"All selled positions: {self.selled_profitable_positions if self.selled_profitable_positions else 'none'}")
        print(f"Own positions: ({len(self.own_positions)}) - {self.own_positions}")
        print(f"Income by selled positions: {self.income_of_selled_positions}")
        print(f"Income after selling all positions: {income_of_owned_positions}")

        if total_income > 0:
            print(f"Total income: \033[92m{total_income}\033[0m\n")  # Green color
        elif total_income == 0:
            print(f"Total income: {total_income}\n")  # White color
        else:
            print(f"Total income: \033[91m{total_income}\033[0m\n")  # Red color

    def get_currency_price(self):
        return BinanceClient(self.currency_for_trading).get_currency_price()

    @staticmethod
    def get_current_time():
        return time.strftime("%H:%M:%S", time.localtime())


bot = Bot("BTCUSDT")
bot.run_trading_session()


# binance_client = BinanceClient("BTCUSDT")
# binance_client.get_historical_trades()