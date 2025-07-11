# src/utils/logger.py

import logging

logger = logging.getLogger("binance_bot")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("bot.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
