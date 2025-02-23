class FiveTenFifteen:
    """Trading strategy that places buy orders in a decreasing price range 
    with increasing take-profit percentages."""

    def __init__(self, api):
        self.api = api
        self.min_value = 0
        self.max_value = 0

    def start(self, min_value, max_value, amount, symbol):
        """
        Starts the strategy: Places a series of stop-limit orders at decreasing prices.

        :param min_value: Lowest price to place orders.
        :param max_value: Highest price to place orders.
        :param amount: Total amount to invest.
        :param symbol: Trading pair (e.g., "BTCUSDT").
        """
        self.validate(min_value, max_value, amount, symbol)

        existing_strategy = self.strategy_manager.get_strategy(symbol)
        if existing_strategy:
            print(f"Strategy for {symbol} already exists. Placing missing orders...")
        else:
            # Save new strategy in the database
            existing_strategy = self.strategy_manager.save_strategy(symbol, min_value, max_value, amount)

        # Cancel existing orders for safety
        self.cancel_existing_orders(symbol)

        # Get current open orders
        open_orders = self.get_open_orders(symbol)

        # Generate new orders
        stop_limit_order_prices, tp_order_prices = self.generate_order_prices(min_value, max_value)

        # Place new orders and replace missing ones
        self.place_orders(symbol, amount, stop_limit_order_prices, tp_order_prices, open_orders)

    def validate(self, min_value, max_value, amount, symbol):
        """Validates input parameters before starting the strategy."""
        if min_value > max_value:
            raise ValueError("Minimum value should be lower than maximum value.")

        current_price = self.api.get_current_value(symbol)
        if min_value > current_price:
            raise ValueError("Minimum value should be lower than the current price of the asset.")

        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        balance = self.api.get_balance("USDT")
        if balance < amount:
            raise ValueError("Insufficient balance for the given amount.")

        if not symbol:
            raise ValueError("Symbol cannot be empty.")

    def cancel_existing_orders(self, symbol):
        """Cancels all open orders before starting the strategy to avoid conflicts."""
        open_orders, err = self.api.get_open_orders(symbol)
        if err:
            raise Exception(f"Error fetching open orders: {err}")

        for order in open_orders:
            self.api.cancel_order(order['orderId'], symbol)

    def get_open_orders(self, symbol):
        """Returns a list of currently open orders for the given symbol."""
        open_orders, err = self.api.get_open_orders(symbol)
        if err:
            raise Exception(f"Error fetching open orders: {err}")
        return open_orders

    def generate_order_prices(self, min_value, max_value):
        """Generates stop-limit order prices and corresponding take-profit prices."""
        stop_limit_order_prices = [max_value]
        tp_order_prices = [max_value * 1.05]  # 5% TP for the highest order

        lower_price = max_value * 0.95  # 5% lower
        decrease_by = max_value - lower_price

        while lower_price >= min_value:
            stop_limit_order_prices.append(lower_price)
            tp_order_prices.append(lower_price)
            lower_price -= decrease_by  # Reduce price by the same value each iteration

        return stop_limit_order_prices, tp_order_prices

    def place_orders(self, symbol, amount, stop_limit_prices, tp_prices, open_orders):
        """Places stop-limit buy and corresponding sell (take-profit) orders."""
        existing_prices = {float(order["price"]) for order in open_orders}

        order_count = len(stop_limit_prices)
        for i, stop_price in enumerate(stop_limit_prices):
            if stop_price in existing_prices:
                continue  # Skip placing duplicate orders

            order_quantity = amount / order_count / stop_price

            # Place stop-limit buy order
            self.api.place_stop_limit_order(symbol, "BUY", order_quantity, stop_price, stop_price * 1.001)

            # Place take-profit sell order
            tp_price = tp_prices[i]
            self.api.place_stop_limit_order(symbol, "SELL", order_quantity, stop_price, tp_price)

    def get_tracked_orders(self, symbol):
        """Fetch orders from Binance and update local DB before returning open orders."""
        # Fetch open orders from Binance
        binance_orders = self.api.get_open_orders(symbol)  # API call to Binance

        # Fetch tracked orders from the database
        db_orders = self.db.query(Order).filter(Order.symbol == symbol).all()

        binance_order_ids = {order["orderId"] for order in binance_orders}  # Binance open orders
        db_order_ids = {order.order_id for order in db_orders}  # Orders in DB

        # Update or delete orders in the database
        for order in db_orders:
            if order.order_id not in binance_order_ids:
                # If an order is missing from Binance, assume it's filled or canceled
                status = self.api.get_order_status(symbol, order.order_id)  # Get actual status
                if status == "FILLED" or status == "CANCELED":
                    self.db.delete(order)  # Remove from local DB
                    self.db.commit()

        return self.db.query(Order).filter(Order.symbol == symbol, Order.status == "OPEN").all()

