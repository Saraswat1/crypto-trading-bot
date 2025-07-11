import argparse
import time
import sys
import os

# Allow importing from src/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binance.client import Client
from binance.exceptions import BinanceAPIException
from config import API_KEY, API_SECRET
from utils.logger import logger


def grid_trading(client, symbol, side, start_price, end_price, steps, qty):
    try:
        prices = [round(start_price + i * ((end_price - start_price) / (steps - 1)), 2) for i in range(steps)]
        logger.info(f"[GRID Strategy] {side} {qty} {symbol} | Prices: {prices}")

        for i, price in enumerate(prices):
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=qty,
                price=str(price)
            )
            print(f"✅ Grid Order {i + 1}/{steps} placed at {price}")
            logger.info(f"Grid Order {i + 1}: {order}")
            time.sleep(0.5)

    except BinanceAPIException as e:
        logger.error(f"Binance API Error (GRID): {e}")
        print("❌ API Error:", e)
    except Exception as e:
        logger.error(f"Grid Strategy Error: {e}")
        print("❌ General Error:", e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", choices=["BUY", "SELL"], required=True)
    parser.add_argument("--qty", type=float, required=True)
    parser.add_argument("--start_price", type=float, required=True)
    parser.add_argument("--end_price", type=float, required=True)
    parser.add_argument("--steps", type=int, default=5)

    args = parser.parse_args()

    client = Client(API_KEY, API_SECRET)
    client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

    grid_trading(
        client,
        args.symbol,
        args.side,
        args.start_price,
        args.end_price,
        args.steps,
        args.qty
    )


if __name__ == "__main__":
    main()
