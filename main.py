# main.py
from spy_backtest.data_handler import fetch_spy_data
from spy_backtest.visualizer import create_dash_app
from spy_backtest.backtest_logic import run_backtest
from spy_backtest.logger import setup_logger

logger = setup_logger("main")

def main():
    try:
        logger.info("Starting SPY Investment Strategy Backtest.")

        history = fetch_spy_data()
        if history.empty:
            logger.error("Failed to fetch SPY data.")
            return

        contributions_df = run_backtest(history, 1000, 100)  # Defaults for testing
        app = create_dash_app(contributions_df)

        logger.info("Launching Dash app.")
        app.run_server(debug=True)

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
