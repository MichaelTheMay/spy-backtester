# data_handler.py
import yfinance as yf
import pandas as pd
from .logger import setup_logger

logger = setup_logger("data_handler")

def fetch_spy_data():
    """
    Fetch historical SPY data from Yahoo Finance and resample to monthly closing prices.

    Returns:
        pd.DataFrame: A DataFrame containing monthly closing prices for SPY.
    """
    try:
        logger.info("Fetching SPY data from Yahoo Finance.")
        spy = yf.Ticker("SPY")
        history = spy.history(period="max")
        history = history.resample('M').last()

        if 'Close' not in history:
            raise ValueError("Missing 'Close' column in fetched data")

        logger.info("Successfully fetched and processed SPY data.")
        return history

    except Exception as e:
        logger.error(f"Error fetching SPY data: {e}")
        return pd.DataFrame()