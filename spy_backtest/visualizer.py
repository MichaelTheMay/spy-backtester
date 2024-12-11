
# visualizer.py
import plotly.graph_objs as go
from dash import Dash, dcc, html
from .logger import setup_logger

logger = setup_logger("visualizer")

def create_dash_app(contributions_df):
    """
    Create a Dash app to visualize the backtest results.

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

            dcc.Graph(
                id="contributions-graph",
                figure={
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
            )
        ])

        logger.info("Dash app successfully created.")
        return app

    except Exception as e:
        logger.error(f"Error creating Dash app: {e}")
        raise