import config

class SimpleStrategy:
    def __init__(self, api):
        self.api = api
        self.entry_price = 0

    # Buy if the price there was no position created before
    def should_buy(self):
        print("should buy")
        value = self.entry_price == 0
        print(value, "value1")
        return value 

    # Sell if the price grew by Y%
    def should_sell(self, current_price):
        print("should sell")
        value = self.entry_price != 0 and current_price > self.entry_price * (1 + config.TAKE_PROFIT_PERCENT)
        print(value, "value2")
        return value

    def execute_trade(self):
        print("execute")
        current_price = self.api.get_price(config.TRADE_SYMBOL)
        
        if self.should_buy():
            print(f"Buying for {current_price}")
            self.api.place_order(config.TRADE_SYMBOL, "BUY", config.TRADE_QUANTITY)
            self.entry_price = current_price

        elif self.should_sell(current_price):
            print(f"Selling for {current_price}")
            self.api.place_order(config.TRADE_SYMBOL, "SELL", config.TRADE_QUANTITY)
            self.entry_price = None # Reset the position
