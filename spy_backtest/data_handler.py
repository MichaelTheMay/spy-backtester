import yfinance as yf
import pandas as pd

def fetch_spy_data():
    """
    Fetch historical SPY data from Yahoo Finance and resample to monthly closing prices.

    Returns:
        pd.DataFrame: A DataFrame containing monthly closing prices for SPY.
    """
    try:
        # Initialize the SPY ticker using yfinance
        spy = yf.Ticker("SPY")

        # Fetch the historical market data for SPY with the maximum available period
        history = spy.history(period="max")

        # Resample the data to monthly intervals, keeping the last closing price of each month
        # Resampling helps in simplifying the analysis for long-term investment backtesting
        history = history.resample('M').last()

        # Ensure the 'Close' column exists in the data; it's essential for backtesting
        if 'Close' not in history:
            raise ValueError("Missing 'Close' column in fetched data")

        # Return the processed DataFrame containing monthly closing prices
        return history

    except Exception as e:
        # Print an error message if any issue occurs during data fetching or processing
        print(f"Error fetching SPY data: {e}")
        
        # Return an empty DataFrame to ensure the program doesn't crash
        return pd.DataFrame()