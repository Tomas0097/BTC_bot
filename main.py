from binance import Client, ThreadedWebsocketManager


class BinanceClient:
    API_KEY = "lbhqUY1k95VIH2x0ahLLD78M40j4v9nUjJoYxaXCekpm80Xsenb9ujUO5IpryOOQ"
    API_SECRET = "nxUn2pKY4p1P1Z84hgveal2ZAkmf6OR9M4K5Oo0J7gv6HJjFWLbCoG1o4JmSyX5q"

    # USDT is a cryptocurrency that is backed 1-to-1 with dollar.
    BTC_IN_USDT_SYMBOL = "BTCUSDT"

    def __init__(self):
        # Connect to binance web socket
        self.binance_web_socket = ThreadedWebsocketManager(api_key=self.API_KEY, api_secret=self.API_SECRET)
        self.binance_web_socket.start()

        # Set up connection with binance API
        self.client = Client(self.API_KEY, self.API_SECRET)

    def get_btc_price(self):
        return self.client.get_avg_price(symbol=self.BTC_IN_USDT_SYMBOL)["price"]

    def get_btc_price_real_time(self):
        self.binance_web_socket.start_trade_socket(callback=self.handle_socket_message, symbol=self.BTC_IN_USDT_SYMBOL)

    @staticmethod
    def handle_socket_message(msg):
        print(f"BTC price in USDT: {msg['p']}")


binance_client = BinanceClient()
# binance_client.get_btc_price_real_time()
print(binance_client.get_btc_price())

