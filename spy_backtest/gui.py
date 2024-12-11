from dash import Dash, dcc, html, Input, Output, State
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
        html.H1("SPY Investment Strategy Backtest", style={"textAlign": "center", "font-family": "Arial, sans-serif", "margin-bottom": "20px"}),
        html.Div([
            html.Div([
                html.Label("Main Strategy: Initial Contribution ($):", style={"font-weight": "bold", "font-family": "Arial, sans-serif"}),
                dcc.Input(id="initial-contribution", type="number", value=1000, step=100, style={"margin-bottom": "10px"}),
                html.Label("Main Strategy: Monthly Contribution ($):", style={"font-weight": "bold", "font-family": "Arial, sans-serif"}),
                dcc.Input(id="monthly-contribution", type="number", value=100, step=10, style={"margin-bottom": "10px"}),
                html.Label("Custom Start Date (YYYY-MM-DD):", style={"font-family": "Arial, sans-serif"}),
                dcc.Input(id="start-date", type="text", value="2000-01-01", style={"margin-bottom": "10px"}),
                html.Label("Custom End Date (YYYY-MM-DD):", style={"font-family": "Arial, sans-serif"}),
                dcc.Input(id="end-date", type="text", value="2020-01-01", style={"margin-bottom": "10px"})
            ], style={"width": "45%", "display": "inline-block", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "background-color": "#f9f9f9", "vertical-align": "top"}),

            html.Div([
                html.Label("Alternative Strategy: Initial Contribution ($):", style={"font-weight": "bold", "font-family": "Arial, sans-serif"}),
                dcc.Input(id="alt-initial-contribution", type="number", value=1000, step=100, style={"margin-bottom": "10px"}),
                html.Label("Alternative Strategy: Monthly Contribution ($):", style={"font-weight": "bold", "font-family": "Arial, sans-serif"}),
                dcc.Input(id="alt-monthly-contribution", type="number", value=200, step=10, style={"margin-bottom": "10px"}),
                html.Button("Run Backtest", id="run-backtest", n_clicks=0, style={"margin-top": "10px", "background-color": "#007BFF", "color": "white", "border": "none", "padding": "10px 15px", "border-radius": "5px", "cursor": "pointer"})
            ], style={"width": "45%", "display": "inline-block", "padding": "10px", "border": "1px solid #ddd", "border-radius": "5px", "background-color": "#f9f9f9", "vertical-align": "top"})
        ], style={"margin-bottom": "20px", "display": "flex", "justify-content": "space-between"}),

        dcc.Graph(id="contributions-graph", style={"border": "1px solid #ddd", "border-radius": "5px", "padding": "10px", "background-color": "#fff"}),
        html.Div(id="backtest-result", style={"textAlign": "center", "margin-top": "20px", "font-family": "Arial, sans-serif", "font-size": "16px", "color": "#333"})
    ])

    @app.callback(
        [Output("contributions-graph", "figure"),
        Output("backtest-result", "children")],
        [Input("run-backtest", "n_clicks")],
        [State("initial-contribution", "value"),
        State("monthly-contribution", "value"),
        State("start-date", "value"),
        State("end-date", "value"),
        State("alt-initial-contribution", "value"),
        State("alt-monthly-contribution", "value")]
    )
    def update_graph(n_clicks, initial_contribution, monthly_contribution, start_date, end_date, alt_initial_contribution, alt_monthly_contribution):
        if n_clicks > 0:
            try:
                logger.info("Executing backtest via GUI.")
                history = fetch_spy_data()
                if history.empty:
                    return {}, "Error fetching SPY data."

                # Filter historical data by custom date range
                history = history.loc[start_date:end_date]
                if history.empty:
                    return {}, "No data available for the specified date range."

                # Main strategy
                contributions_df = run_backtest(history, initial_contribution, monthly_contribution)
                main_fig = create_plot_figure(contributions_df)

                # Alternative strategy (if provided)
                if alt_initial_contribution and alt_monthly_contribution:
                    alt_contributions_df = run_backtest(history, alt_initial_contribution, alt_monthly_contribution)
                    alt_fig = create_plot_figure(alt_contributions_df)

                    # Combine figures - ensure data is a list
                    if not isinstance(main_fig["data"], list):
                        main_fig["data"] = list(main_fig["data"])
                    
                    # Add alternative strategy traces
                    if isinstance(alt_fig["data"], list):
                        main_fig["data"].extend(alt_fig["data"])
                    else:
                        main_fig["data"].extend(list(alt_fig["data"]))
                    
                    main_fig["layout"].update(title="Portfolio Value vs Contributions (Comparison)")

                return main_fig, "Backtest complete!"# Main strategy
               

            except Exception as e:
                logger.error(f"Error in GUI callback: {e}")
                return {}, "An error occurred. Please try again."

        return {}, "Click 'Run Backtest' to execute."

    return app
