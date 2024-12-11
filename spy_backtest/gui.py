from dash import Dash, dcc, html, Input, Output
from .visualizer import create_plot_figure
from .data_handler import fetch_spy_data
from .backtest_logic import run_backtest
from .logger import setup_logger

logger = setup_logger("gui")

def create_dash_app():
    """
    Sets up the Dash app, including layout and callbacks.
    
    Returns:
        Dash: The configured Dash application.
    """
    logger.info("Setting up Dash app.")
    app = Dash(__name__)

    # App layout
    app.layout = html.Div([
        html.H1("SPY Investment Strategy Backtest", style={"textAlign": "center"}),
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

    # Callbacks
    @app.callback(
        [Output("contributions-graph", "figure"),
         Output("backtest-result", "children")],
        [Input("run-backtest", "n_clicks"),
         Input("initial-contribution", "value"),
         Input("monthly-contribution", "value")]
    )
    def update_graph(n_clicks, initial_contribution, monthly_contribution):
        if n_clicks > 0:
            try:
                logger.info("Executing backtest via GUI.")
                history = fetch_spy_data()
                if history.empty:
                    return {}, "Error fetching SPY data."

                contributions_df = run_backtest(history, initial_contribution, monthly_contribution)
                fig = create_plot_figure(contributions_df)

                return fig, "Backtest complete!"
            except Exception as e:
                logger.error(f"Error in GUI callback: {e}")
                return {}, "An error occurred. Please try again."

        return {}, "Click 'Run Backtest' to execute."

    return app
