# File: src/advanced/oco.py

import argparse
import time
import sys
import os

# Allow importing from src/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from config import API_KEY, API_SECRET
from utils.logger import logger


def place_simulated_oco(client, symbol, qty, take_profit_price, stop_price):
    try:
        # Place take-profit LIMIT order
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=qty,
            price=str(take_profit_price)
        )
        logger.info(f"[OCO] Take-profit order placed: {tp_order['orderId']} at {take_profit_price}")
        print(f"[SUCCESS] Take-profit order placed at {take_profit_price}")

        # Place stop-market order
        stop_order = client.futures_create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_STOP_MARKET,
            stopPrice=str(stop_price),
            closePosition=True,
            timeInForce=TIME_IN_FORCE_GTC
        )
        logger.info(f"[OCO] Stop-loss order placed: {stop_order['orderId']} at {stop_price}")
        print(f"[SUCCESS] Stop-loss (market) order placed at stop price {stop_price}")

        print("[INFO] Note: You must cancel the opposite order manually once one is filled.")

    except BinanceAPIException as e:
        logger.error(f"[ERROR] Binance API Error (Simulated OCO): {e}")
        print("[ERROR] Binance API error:", e)
    except Exception as e:
        logger.error(f"[ERROR] OCO Simulation Error: {e}")
        print("[ERROR] General error:", e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--qty", type=float, required=True)
    parser.add_argument("--take_profit", type=float, required=True)
    parser.add_argument("--stop_price", type=float, required=True)

    args = parser.parse_args()

    client = Client(API_KEY, API_SECRET)
    client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

    place_simulated_oco(client, args.symbol, args.qty, args.take_profit, args.stop_price)


if __name__ == "__main__":
    main()
