import matplotlib.pyplot as plt

def plot_contributions(contributions_df):
    """
    Plot the total contributions and total portfolio value over time.

    Args:
        contributions_df (pd.DataFrame): DataFrame containing 'Total Contributions' and 'Total Value'.

    Returns:
        matplotlib.figure.Figure: A Matplotlib figure object.
    """
    # Create a new figure and axis for the plot
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot total contributions and total value from the DataFrame
    contributions_df.plot(ax=ax, color=["blue", "green"], linewidth=2)

    # Add labels, title, and grid for better readability
    ax.set_title("Investment Backtest Results", fontsize=14)
    ax.set_xlabel("Months", fontsize=12)
    ax.set_ylabel("Value ($)", fontsize=12)
    ax.legend(["Total Contributions", "Total Value"], fontsize=10)
    ax.grid(True)

    # Return the figure object for rendering in the GUI
    return fig