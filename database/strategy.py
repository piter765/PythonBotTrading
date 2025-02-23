from sqlalchemy.orm import Session
from models.strategy import Strategy

class StrategyManager:
    """Handles strategy storage and retrieval."""

    def __init__(self, db: Session):
        self.db = db

    def save_strategy(self, symbol: str, min_value: float, max_value: float, amount: float):
        """Saves a new strategy in the database."""
        strategy = Strategy(symbol=symbol, min_value=min_value, max_value=max_value, amount=amount)
        self.db.add(strategy)
        self.db.commit()
        self.db.refresh(strategy)
        return strategy

    def get_strategy(self, symbol: str):
        """Retrieves a strategy by symbol."""
        return self.db.query(Strategy).filter(Strategy.symbol == symbol, Strategy.active == True).first()

    def deactivate_strategy(self, strategy_id: int):
        """Deactivates a strategy instead of deleting it."""
        strategy = self.db.query(Strategy).filter(Strategy.id == strategy_id).first()
        if strategy:
            strategy.active = False
            self.db.commit()
        return strategy
