import argparse
import time
import sys
import os
import pandas as pd

# Allow importing from src/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binance.client import Client
from binance.exceptions import BinanceAPIException
from config import API_KEY, API_SECRET
from utils.logger import logger


def twap_live(client, symbol, side, qty, chunks=4, delay=5):
    chunk_qty = round(qty / chunks, 6)
    logger.info(f"[TWAP Live] {side} {qty} {symbol} in {chunks} chunks")

    for i in range(chunks):
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=chunk_qty
            )
            print(f"✅ TWAP Live Chunk {i + 1}: Executed {chunk_qty} {symbol}")
            logger.info(f"TWAP Live Chunk {i + 1} Executed: {order}")
            time.sleep(delay)
        except BinanceAPIException as e:
            logger.error(f"Binance API Error (TWAP): {e}")
            print("❌ API Error:", e)
            break
        except Exception as e:
            logger.error(f"TWAP General Error: {e}")
            break


def twap_simulated(symbol, side, qty, csv_path="historical_data.csv"):
    try:
        df = pd.read_csv(csv_path)
        prices = df['close'].tolist()[:4]  # Simulate with first 4 close prices
        chunk_qty = round(qty / 4, 6)

        logger.info(f"[TWAP Simulated] {side} {qty} {symbol} using {csv_path}")
        for i, price in enumerate(prices):
            print(f"🧪 Simulated TWAP Chunk {i + 1}: {chunk_qty} {symbol} at price {price}")
            logger.info(f"Simulated TWAP at price {price} for chunk {i + 1}")
            time.sleep(1)
    except Exception as e:
        logger.error(f"Failed to simulate TWAP: {e}")
        print("❌ Error loading or simulating historical data")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", choices=["BUY", "SELL"], required=True)
    parser.add_argument("--qty", type=float, required=True)
    parser.add_argument("--simulate", action='store_true')
    parser.add_argument("--csv", default="historical_data.csv")

    args = parser.parse_args()

    if args.simulate:
        twap_simulated(args.symbol, args.side, args.qty, args.csv)
    else:
        client = Client(API_KEY, API_SECRET)
        client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        twap_live(client, args.symbol, args.side, args.qty)


if __name__ == "__main__":
    main()
