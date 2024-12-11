# Update in main.py
from spy_backtest.gui import create_dash_app
from spy_backtest.logger import setup_logger

logger = setup_logger("main")

def main():
    try:
        logger.info("Launching the Dash application.")
        app = create_dash_app()
        app.run_server(debug=True)
    except Exception as e:
        logger.error(f"Failed to launch the application: {e}")

if __name__ == "__main__":
    main()