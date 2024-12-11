import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from spy_backtest.data_handler import fetch_spy_data
from spy_backtest.visualizer import plot_contributions

def validate_input(input_value):
    """
    Validate that the input is a positive numeric value.

    Args:
        input_value (str): The input value from the user.

    Returns:
        float: The validated numeric value.

    Raises:
        ValueError: If the input is invalid.
    """
    try:
        value = float(input_value)
        if value < 0:
            raise ValueError("Value cannot be negative.")
        return value
    except ValueError:
        raise ValueError("Invalid input. Please enter a positive number.")

def backtest():
    try:
        # Get and validate user inputs from GUI
        initial_contribution = validate_input(initial_contribution_var.get())
        monthly_contribution = validate_input(monthly_contribution_var.get())

        # Fetch SPY historical data
        history = fetch_spy_data()
        if history.empty:
            result_label.config(text="Error fetching data. Check connection.", foreground="red")
            return

        # Backtest logic
        contributions = []
        total_contributions = initial_contribution
        total_value = initial_contribution
        share_count = initial_contribution / history['Close'].iloc[0]

        for price in history['Close'][1:]:
            total_contributions += monthly_contribution
            share_count += monthly_contribution / price
            total_value = share_count * price
            contributions.append((total_contributions, total_value))

        # Create DataFrame for plotting
        contributions_df = pd.DataFrame(contributions, columns=["Total Contributions", "Total Value"])

        # Generate plot using visualizer module
        fig = plot_contributions(contributions_df)

        # Display the plot in the GUI
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

        # Update result label
        result_label.config(text="Backtest complete!", foreground="green")
    except ValueError as e:
        result_label.config(text=str(e), foreground="red")

# Create the GUI
root = tk.Tk()
root.title("SPY Investment Strategy Backtest")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Initial contribution input
initial_contribution_var = tk.StringVar(value="1000")
initial_contribution_label = ttk.Label(frame, text="Initial Contribution ($):")
initial_contribution_label.grid(row=0, column=0, sticky=tk.W)
initial_contribution_entry = ttk.Entry(frame, textvariable=initial_contribution_var)
initial_contribution_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

# Monthly contribution input
monthly_contribution_var = tk.StringVar(value="100")
monthly_contribution_label = ttk.Label(frame, text="Monthly Contribution ($):")
monthly_contribution_label.grid(row=1, column=0, sticky=tk.W)
monthly_contribution_entry = ttk.Entry(frame, textvariable=monthly_contribution_var)
monthly_contribution_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

# Backtest button
backtest_button = ttk.Button(frame, text="Run Backtest", command=backtest)
backtest_button.grid(row=2, column=0, columnspan=2)

# Result label
result_label = ttk.Label(frame, text="", font=("Arial", 10))
result_label.grid(row=3, column=0, columnspan=2)

# Padding for better spacing
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
