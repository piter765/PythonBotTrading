from binance.client import Client
import config

class BinanceAPI:
    def __init__(self, testnet=True):
        self.client = Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, testnet=testnet)

    def get_price(self, symbol):
        """Gets current price of a symbol"""
        return float(self.client.get_symbol_ticker(symbol=symbol)['price'])

    def place_market_order(self, symbol, side, quantity):
        print("placing order")
        order = self.client.order_market(symbol=symbol, side=side, quantity=quantity)
        print(order, "order")
        return order
    
    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type="STOP_LOSS_LIMIT",
                quantity=quantity,
                price=str(limit_price),
                stopPrice=str(stop_price),
                timeInForce="GTC"  # Good-Til-Cancelled (remains open until filled/canceled)
            )
            return order  # Returns order details
        except Exception as e:
            print(f"Error placing stop-limit order: {e}")
            return None  # Returns None on failure

    def get_balance(self, asset="USDT"):
        """Gets account balance"""
        return float(self.client.get_asset_balance(asset=asset)['free'])
    
    def get_open_orders(self, symbol):
        """Gets open orders on asset"""
        try:
            return self.client.get_open_orders(symbol=symbol), None
        except Exception as e:
            print(f"Error fetching open orders: {e}")
            return [], e
