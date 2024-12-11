import plotly.graph_objs as go
from .logger import setup_logger

logger = setup_logger("visualizer")

def create_plot_figure(contributions_df):
    """
    Generate a Plotly figure for the contributions and portfolio value.
    
    Args:
        contributions_df (pd.DataFrame): DataFrame with 'Total Contributions' and 'Total Value'.
        
    Returns:
        dict: Plotly figure dictionary.
    """
    try:
        logger.info("Creating plot figure.")
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
        logger.info("Figure successfully created.")
        return fig
    except Exception as e:
        logger.error(f"Error creating plot figure: {e}")
        raise
