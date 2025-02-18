import os
from dotenv import load_dotenv

# Wczytanie kluczy API
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Ustawienia handlu
TRADE_SYMBOL = "BTCUSDT"
TRADE_QUANTITY = 0.001  # Ilość BTC do zakupu
STOP_LOSS_PERCENT = 0.02  # 2% stop-loss
TAKE_PROFIT_PERCENT = 0.01  # 1% take-profit

# Spot API URL

# Spot Test Network URL

# https://api.binance.com/api	https://testnet.binance.vision/api
# wss://stream.binance.com:9443/ws	wss://testnet.binance.vision/ws
# wss://stream.binance.com:9443/stream	wss://testnet.binance.vision/stream
