# src/limit_orders.py

import argparse
from binance.client import Client
from binance.exceptions import BinanceAPIException
from utils.logger import logger
from config import API_KEY, API_SECRET


def place_limit_order(symbol, side, quantity, price):
    try:
        client = Client(API_KEY, API_SECRET)
        client.API_URL = 'https://testnet.binancefuture.com/fapi'

        logger.info(f"Placing limit order: {side} {quantity} {symbol} at {price}")
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=str(price)
        )
        logger.info(f"Limit order successful: {order}")
        print("✅ Limit order executed successfully!")
        print(order)

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: {e}")
        print(f"❌ Binance API error: {e}")
    except Exception as e:
        logger.error(f"General Error: {e}")
        print(f"❌ Error: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Place a LIMIT order on Binance Futures Testnet")
    parser.add_argument("symbol", help="Trading pair, e.g., BTCUSDT")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("quantity", type=float, help="Order quantity")
    parser.add_argument("price", type=float, help="Limit price")

    args = parser.parse_args()
    place_limit_order(args.symbol, args.side, args.quantity, args.price)
