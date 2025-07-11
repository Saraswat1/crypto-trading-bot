# src/market_orders.py

import argparse
from binance.client import Client
from binance.exceptions import BinanceAPIException
from utils.logger import logger
from config import API_KEY, API_SECRET


def place_market_order(symbol, side, quantity):
    try:
        client = Client(API_KEY, API_SECRET)
        client.API_URL = 'https://testnet.binancefuture.com/fapi'

        logger.info(f"Placing market order: {side} {quantity} {symbol}")
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='MARKET',
            quantity=quantity
        )
        logger.info(f"Market order successful: {order}")
        print("✅ Market order executed successfully!")
        print(order)

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: {e}")
        print(f"❌ Binance API error: {e}")
    except Exception as e:
        logger.error(f"General Error: {e}")
        print(f"❌ Error: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Place a MARKET order on Binance Futures Testnet")
    parser.add_argument("symbol", help="Trading pair, e.g., BTCUSDT")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("quantity", type=float, help="Order quantity")

    args = parser.parse_args()
    place_market_order(args.symbol, args.side, args.quantity)
