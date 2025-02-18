import config

class RiskManager:
    def __init__(self, balance):
        self.initial_balance = balance

    def check_risk(self, current_balance):
        """Stopping the bot if it lost more than 10% of the capital"""
        max_drawdown = self.initial_balance * 0.90
        if current_balance < max_drawdown:
            print("Bot is stopping.")
            return False
        return True
