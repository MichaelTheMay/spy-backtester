# visualizer.py
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
from .logger import setup_logger

logger = setup_logger("visualizer")

def create_dash_app(contributions_df):
    """
    Create a Dash app to visualize the backtest results and include user inputs for contributions.

    Args:
        contributions_df (pd.DataFrame): DataFrame containing 'Total Contributions' and 'Total Value'.

    Returns:
        Dash: A Dash application.
    """
    try:
        logger.info("Creating Dash app for contributions and portfolio value visualization.")
        app = Dash(__name__)

        app.layout = html.Div([
            html.H1("SPY Investment Backtest Results", style={"textAlign": "center"}),

            html.Div([
                html.Label("Initial Contribution ($):"),
                dcc.Input(id="initial-contribution", type="number", value=1000, step=100),
                html.Label("Monthly Contribution ($):"),
                dcc.Input(id="monthly-contribution", type="number", value=100, step=10),
                html.Button("Run Backtest", id="run-backtest", n_clicks=0)
            ], style={"margin-bottom": "20px"}),

            dcc.Graph(id="contributions-graph"),

            html.Div(id="backtest-result", style={"textAlign": "center", "margin-top": "20px"})
        ])

        @app.callback(
            [Output("contributions-graph", "figure"),
             Output("backtest-result", "children")],
            [Input("run-backtest", "n_clicks")],
            [Input("initial-contribution", "value"),
             Input("monthly-contribution", "value")]
        )
        def update_backtest(n_clicks, initial_contribution, monthly_contribution):
            if n_clicks > 0:
                try:
                    logger.info("Running backtest from web input.")
                    from .data_handler import fetch_spy_data
                    from .backtest_logic import run_backtest

                    history = fetch_spy_data()
                    if history.empty:
                        return {}, "Error fetching SPY data. Please try again."

                    contributions_df = run_backtest(history, initial_contribution, monthly_contribution)

                    fig = {
                        "data": [
                            go.Scatter(
                                x=contributions_df.index,
                                y=contributions_df["Total Contributions"],
                                mode="lines",
                                name="Total Contributions",
                                line=dict(color="blue", width=2)
                            ),
                            go.Scatter(
                                x=contributions_df.index,
                                y=contributions_df["Total Value"],
                                mode="lines",
                                name="Total Portfolio Value",
                                line=dict(color="green", width=2)
                            )
                        ],
                        "layout": go.Layout(
                            title="Portfolio Value vs Contributions",
                            xaxis=dict(title="Date", tickformat="%Y"),
                            yaxis=dict(title="Value ($)"),
                            template="plotly_white"
                        )
                    }

                    return fig, "Backtest complete!"

                except Exception as e:
                    logger.error(f"Error during backtest: {e}")
                    return {}, "An error occurred during backtesting."

            return {}, "Click 'Run Backtest' to begin."

        logger.info("Dash app successfully created.")
        return app

    except Exception as e:
        logger.error(f"Error creating Dash app: {e}")
        raise