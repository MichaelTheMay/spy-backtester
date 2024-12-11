# backtest_logic.py
import pandas as pd
from .logger import setup_logger

logger = setup_logger("backtest_logic")

def run_backtest(history, initial_contribution, monthly_contribution):
    """
    Run the backtest logic based on historical data and user inputs.

    Args:
        history (pd.DataFrame): Historical SPY data with 'Close' column.
        initial_contribution (float): Initial contribution amount.
        monthly_contribution (float): Monthly contribution amount.

    Returns:
        pd.DataFrame: DataFrame with 'Total Contributions', 'Total Value', and 'Market Gains'.
    """
    try:
        logger.info("Starting backtest.")
        contributions = []
        total_contributions = initial_contribution
        total_value = initial_contribution
        market_gains = 0
        share_count = initial_contribution / history['Close'].iloc[0]

        for i, price in enumerate(history['Close'][1:], start=1):
            total_contributions += monthly_contribution
            share_count += monthly_contribution / price

            # Calculate portfolio value based on current share count
            total_value = share_count * price

            # Calculate market gains (value - contributions)
            market_gains = total_value - total_contributions

            contributions.append((total_contributions, total_value, market_gains))

        contributions_df = pd.DataFrame(
            contributions, 
            columns=["Total Contributions", "Total Value", "Market Gains"], 
            index=history.index[1:]
        )
        logger.info("Backtest successfully completed.")
        return contributions_df

    except Exception as e:
        logger.error(f"Error during backtest: {e}")
        raise
