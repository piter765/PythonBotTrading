from binance.client import Client
import config

class BinanceAPI:
    def __init__(self, testnet=True):
        self.client = Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, testnet=testnet)

    def get_price(self, symbol):
        """Pobiera aktualną cenę instrumentu"""
        return float(self.client.get_symbol_ticker(symbol=symbol)['price'])

    def place_order(self, symbol, side, quantity):
        print("placing order")
        order = self.client.order_market(symbol=symbol, side=side, quantity=quantity)
        print(order, "order")
        return order

    def get_balance(self, asset):
        """Pobiera saldo danego aktywa"""
        return float(self.client.get_asset_balance(asset=asset)['free'])
