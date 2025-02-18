import time
from api.binance_api import BinanceAPI
from strategy import SimpleStrategy
from risk_management import RiskManager

def main():
    api = BinanceAPI(testnet=True)
    strategy = SimpleStrategy(api)
    risk_manager = RiskManager(api.get_balance("USDT"))

    while True:
        balance = api.get_balance("USDT")
        print(balance, " balance")
        if not risk_manager.check_risk(balance):
            break

        strategy.execute_trade()
        time.sleep(60) 

if __name__ == "__main__":
    main()
