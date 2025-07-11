# src/advanced/stop_limit.py

import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binance.client import Client
from binance.exceptions import BinanceAPIException
from config import API_KEY, API_SECRET
from utils.logger import logger


def place_stop_limit_order(symbol, side, quantity, stop_price, limit_price):
    try:
        client = Client(API_KEY, API_SECRET)
        client.API_URL = 'https://testnet.binancefuture.com/fapi'

        logger.info(f"Placing STOP-LIMIT order: {side} {quantity} {symbol} Stop={stop_price}, Limit={limit_price}")

        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='STOP',
            timeInForce='GTC',
            quantity=quantity,
            price=str(limit_price),
            stopPrice=str(stop_price)
        )

        logger.info(f"STOP-LIMIT order successful: {order}")
        print("✅ Stop-Limit order placed successfully!")
        print(order)

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: {e}")
        print(f"❌ Binance API error: {e}")
    except Exception as e:
        logger.error(f"General Error: {e}")
        print(f"❌ Error:", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Place a Stop-Limit order on Binance Futures Testnet")
    parser.add_argument("symbol", help="e.g. BTCUSDT")
    parser.add_argument("side", choices=["BUY", "SELL"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("stop_price", type=float)
    parser.add_argument("limit_price", type=float)

    args = parser.parse_args()
    place_stop_limit_order(args.symbol, args.side, args.quantity, args.stop_price, args.limit_price)
