# main.py
import tkinter as tk
from tkinter import simpledialog
from tkinter.scrolledtext import ScrolledText
from metricstics import Metricstics
import random

# The main application script for METRICSTICS, a statistical calculator.
# It provides a GUI for generating random data and calculating various statistics.

# Function to generate random data
def generate_random_values():
    # Ask the user for the number of values to generate within a specified range.
    numeric_val = simpledialog.askinteger("Input", "How many values would you like to generate?", minvalue=1, maxvalue=10000)
    if numeric_val is not None:
        # Generate a list of random integers.
        val = [random.randint(0, 1000) for _ in range(numeric_val)]
        # Clear the current data in the display and show the new random values.
        data_display.delete('1.0', tk.END)
        data_display.insert(tk.END, ', '.join(map(str, val)))

# Function to calculate and display a single metric
def calculate_single_metric(metric_function, label):
    try:
        # Retrieve data from the display, split by commas and convert to integers.
        data_str = data_display.get('1.0', tk.END).strip()
        if not data_str:
            raise ValueError("No data generated.")
        data = list(map(int, data_str.split(',')))
        metrics = Metricstics(data)
        # Use the metric function passed as an argument to calculate the result.
        result = metric_function(metrics)
        # Update the GUI label with the result of the metric calculation.
        label.config(text=f"{metric_function.__name__.capitalize()}: {result}")
    except ValueError as e:
        # If an error occurs, show it in the GUI label.
        label.config(text=f"Error: {e}. Please enter valid numeric data.")

# Function to calculate and display all metrics
def calculate_all_metrics():
    # Retrieve the current data from the display.
    data_str = data_display.get('1.0', tk.END).strip()
    if not data_str:
        # If no data is present, display an error message in each statistic label.
        for label in stats_labels:
            label.config(text="Error: No data present. Please generate data first.")
        return
    # Iterate over each metric function and associated label to update the statistics.
    for metric_function, label in zip(stats_functions, stats_labels):
        calculate_single_metric(metric_function[0], label)

# Function to clear all data and reset all labels
def func_clear_all():
    # Clear the text in the data display widget.
    data_display.delete('1.0', tk.END)
    # Reset each label to show the metric name without any calculated value.
    for label in stats_labels:
        label.config(text=f"{label.cget('text').split(':')[0]}: ")

# Initialize the main window of the application with a title and fixed size.
root = tk.Tk()
root.title('METRICSTICS')
root.geometry('800x600')

# Define styles for buttons, labels, and the data display area.
button_style = {'font': ('Arial', 12), 'bg': '#D3D3D3', 'fg': 'black', 'padx': 10, 'pady': 5}
label_style = {'font': ('Arial', 12), 'bg': '#f0f0f0', 'fg': 'black'}
data_display_style = {'font': ('Consolas', 10), 'bg': '#fff', 'fg': 'black'}

# Create and pack the main frame to hold all other widgets.
main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(expand=True, fill='both', padx=20, pady=20)

# Create and pack a label as the heading of the application.
heading_label = tk.Label(main_frame, text="Welcome to METRICSTICS: A Statistical Calculator", **label_style)
heading_label.pack(pady=(0, 20))

# Create and pack the ScrolledText widget for displaying generated data.
data_display = ScrolledText(main_frame, height=10, width=70, **data_display_style)
data_display.pack(pady=(0, 20))

# Frame to hold action buttons like 'Generate Data', 'Calculate All Metrics', 'Clear All'.
buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
buttons_frame.pack(pady=(0, 10))

# Create and pack buttons within the buttons_frame.
generate_button = tk.Button(buttons_frame, text='Generate Data', command=generate_random_values, **button_style)
generate_button.pack(side=tk.LEFT, padx=5)

calculate_all_button = tk.Button(buttons_frame, text='Calculate All Metrics', command=calculate_all_metrics, **button_style)
calculate_all_button.pack(side=tk.LEFT, padx=5)

clear_all_button = tk.Button(buttons_frame, text='Clear All', command=func_clear_all, **button_style)
clear_all_button.pack(side=tk.LEFT, padx=5)

# Frame to display metrics labels and buttons for individual metric calculations.
metrics_frame = tk.Frame(main_frame, bg='#f0f0f0')
metrics_frame.pack(fill='x', expand=True)

# Define the statistical functions and corresponding labels.
stats_labels = []
stats_functions = [
    (Metricstics.minimum, "Minimum"),
    (Metricstics.maximum, "Maximum"),
    # ... Add other metric functions from Metricstics class ...
]

# Dynamically create and pack labels and buttons for each metric in the metrics_frame.
for i, (func, name) in enumerate(stats_functions):
    label = tk.Label(metrics_frame, text=f"{name}: ", **label_style)
    label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
    stats_labels.append(label)
    button = tk.Button(metrics_frame, text=f"Calculate {name}", command=lambda f=func, l=label: calculate_single_metric(f, l), **button_style)
    button.grid(row=i, column=1, sticky='e', padx=5, pady=2)

# Footer frame for the application's bottom, displaying a label with the team name.
footer_frame = tk.Frame(root, bg='#ddd', height=30)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
footer_frame.pack_propagate(False)

footer_label = tk.Label(footer_frame, text="By Team N", font=('Arial', 10), bg='#ddd', fg='black')
footer_label.pack()

# Start the main loop to run the application.
root.mainloop()
