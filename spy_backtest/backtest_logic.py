
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
        pd.DataFrame: DataFrame with 'Total Contributions' and 'Total Value'.
    """
    try:
        logger.info("Starting backtest.")
        contributions = []
        total_contributions = initial_contribution
        total_value = initial_contribution
        share_count = initial_contribution / history['Close'].iloc[0]

        for price in history['Close'][1:]:
            total_contributions += monthly_contribution
            share_count += monthly_contribution / price
            total_value = share_count * price
            contributions.append((total_contributions, total_value))

        contributions_df = pd.DataFrame(
            contributions, 
            columns=["Total Contributions", "Total Value"], 
            index=history.index[1:]
        )
        logger.info("Backtest successfully completed.")
        return contributions_df

    except Exception as e:
        logger.error(f"Error during backtest: {e}")
        raise