import time
from api.binance_api import BinanceAPI
from strategy import SimpleStrategy
from risk_management import RiskManager
from database.database import Database

def main():
    api = BinanceAPI(testnet=True)
    strategy = SimpleStrategy(api)
    risk_manager = RiskManager(api.get_balance("USDT"))

    # db = Database()

    # db.add_order("BTCUSDT", 0.001, 45000)

    # open_orders = db.get_open_orders()
    # print("Open Orders:", open_orders)

    while True:
        balance = api.get_balance("USDT")
        print(balance, " balance")
        if not risk_manager.check_risk(balance):
            break

        strategy.execute_trade()
        time.sleep(60) 

if __name__ == "__main__":
    main()
