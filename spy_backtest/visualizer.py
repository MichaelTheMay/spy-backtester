# visualizer.py
import plotly.graph_objs as go
from .logger import setup_logger

logger = setup_logger("visualizer")

def create_plot_figure(contributions_df, alt_contributions_df=None):
    """
    Generate a Plotly figure for the contributions and portfolio value.

    Args:
        contributions_df (pd.DataFrame): DataFrame with 'Total Contributions', 'Total Value', and 'Market Gains'.
        alt_contributions_df (pd.DataFrame, optional): DataFrame for an alternative strategy.

    Returns:
        dict: Plotly figure dictionary.
    """
    try:
        logger.info("Creating plot figure.")

        # Main strategy plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=contributions_df.index,
            y=contributions_df["Total Value"],
            mode="lines",
            name="Main Strategy: Total Value",
            line=dict(color="blue", width=2)
        ))
        fig.add_trace(go.Scatter(
            x=contributions_df.index,
            y=contributions_df["Total Contributions"],
            mode="lines",
            name="Main Strategy: Total Contributions",
            line=dict(color="blue", dash="dot")
        ))
        fig.add_trace(go.Scatter(
            x=contributions_df.index,
            y=contributions_df["Total Contributions"],
            fill="tonexty",
            mode="none",
            fillcolor="rgba(0, 0, 255, 0.2)",  # Translucent blue
            name="Main Strategy: Contributions Area"
        ))

        # Alternative strategy plot (if provided)
        if alt_contributions_df is not None:
            fig.add_trace(go.Scatter(
                x=alt_contributions_df.index,
                y=alt_contributions_df["Total Value"],
                mode="lines",
                name="Alt Strategy: Total Value",
                line=dict(color="green", width=2)
            ))
            fig.add_trace(go.Scatter(
                x=alt_contributions_df.index,
                y=alt_contributions_df["Total Contributions"],
                mode="lines",
                name="Alt Strategy: Total Contributions",
                line=dict(color="green", dash="dot")
            ))
            fig.add_trace(go.Scatter(
                x=alt_contributions_df.index,
                y=alt_contributions_df["Total Contributions"],
                fill="tonexty",
                mode="none",
                fillcolor="rgba(0, 128, 0, 0.2)",  # Translucent green
                name="Alt Strategy: Contributions Area"
            ))

        # Highlight market gains area for the main strategy
        fig.add_trace(go.Scatter(
            x=contributions_df.index,
            y=contributions_df["Market Gains"],
            fill="tonexty",
            mode="none",
            fillcolor="rgba(0, 0, 255, 0.1)",  # Lighter translucent blue
            name="Main Strategy: Market Gains"
        ))

        # Highlight market gains area for the alternative strategy (if provided)
        if alt_contributions_df is not None:
            fig.add_trace(go.Scatter(
                x=alt_contributions_df.index,
                y=alt_contributions_df["Market Gains"],
                fill="tonexty",
                mode="none",
                fillcolor="rgba(0, 128, 0, 0.1)",  # Lighter translucent green
                name="Alt Strategy: Market Gains"
            ))

        # Add performance metrics as annotations
        fig.add_annotation(
            x=contributions_df.index[-1],
            y=contributions_df["Total Value"].iloc[-1],
            text=f"Final Value: ${contributions_df['Total Value'].iloc[-1]:,.2f}",
            showarrow=True,
            arrowhead=2,
            ax=-40,
            ay=-40,
            font=dict(color="blue")
        )
        if alt_contributions_df is not None:
            fig.add_annotation(
                x=alt_contributions_df.index[-1],
                y=alt_contributions_df["Total Value"].iloc[-1],
                text=f"Final Value: ${alt_contributions_df['Total Value'].iloc[-1]:,.2f}",
                showarrow=True,
                arrowhead=2,
                ax=-40,
                ay=-40,
                font=dict(color="green")
            )

        # Add a custom tooltip for user interaction
        fig.update_traces(hoverinfo="x+y+name")

        # Update layout for better visualization
        fig.update_layout(
            title="Portfolio Value vs Contributions",
            xaxis=dict(title="Date", tickformat="%Y"),
            yaxis=dict(title="Value ($)"),
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )

        logger.info(f"Figure successfully created: ")
        return fig.to_dict()  # Convert the figure to a dictionary format
    except Exception as e:
        logger.error(f"Figure: {fig}\n\n\nError creating plot figure: {e}")
        raise
