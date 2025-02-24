from sqlalchemy.orm import Session
from models.order import Order  # Import Order model

class OrderManager:
    """Manages order-related database operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_open_orders(self, symbol):
        """Fetch open orders from the database."""
        return self.db.query(Order).filter(Order.symbol == symbol, Order.status == "OPEN").all()

    def sync_with_binance(self, api, symbol):
      """Syncs database orders with Binance and updates their status."""
      binance_orders = api.get_open_orders(symbol)
      db_orders = self.get_open_orders(symbol)

      binance_order_ids = {order["orderId"] for order in binance_orders}

      for order in db_orders:
          if order.order_id not in binance_order_ids:  # Not in open orders → Check status
              status = api.get_order_status(symbol, order.order_id)

              if status in ["FILLED", "CANCELED"]:
                  order.status = status
                  self.db.commit()

    def save_order(self, order_id, symbol, price, quantity, status="OPEN"):
        """Saves a new order in the database."""
        new_order = Order(
            order_id=order_id,
            symbol=symbol,
            price=price,
            quantity=quantity,
            status=status
        )
        self.db.add(new_order)
        self.db.commit()
