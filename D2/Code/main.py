import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from metricstics import Metricstics
import random
import threading
from concurrent.futures import ThreadPoolExecutor
full_dataset = []

# Helper functions to support main application functionality

def ask_for_number_of_values():
    """
        Prompt the user to enter the number of random values to generate.
        Handles any exceptions and shows an error dialog if the input is invalid.
        """
    try:
        numeric_val = simpledialog.askinteger("Input",
                                              "How many values would you like to generate?",
                                              minvalue=1,
                                              maxvalue=30000)
        if numeric_val is not None:
            generate_values(numeric_val)
    except Exception as e:
        messagebox.showerror("Input Error", str(e))

def generate_values(numeric_val):
    """
        Generates a specified number of random values and updates the data display.
        """
    val = [random.randint(0, 1000) for _ in range(numeric_val)]
    update_data_display(val)
    show_status_message(f"{numeric_val} values generated.")

def update_data_display(values):
    """
        Updates the ScrolledText widget with a list of values.
        """
    global full_dataset  # Maximum number of values to display
    full_dataset = values

    MAX_DISPLAY = 1000
    if len(values) > MAX_DISPLAY:
        # Show a summary of the data
        summary_text = f"Total values: {len(values)}\n" \
                       f"First {MAX_DISPLAY} values: \n" + \
                       ', '.join(map(str, values[:MAX_DISPLAY])) + "\n...\n" + \
                       "(Displaying a subset due to large data size)"
        data_display.delete('1.0', tk.END)
        data_display.insert(tk.END, summary_text)
    else:
        # Show all values
        display_text = ', '.join(map(str, values))
        data_display.delete('1.0', tk.END)
        data_display.insert(tk.END, display_text)
#Function to retrieve data

def retrieve_data():
    if not full_dataset:
        raise ValueError("No data generated.")
    return full_dataset

def update_label_with_result(label, result):
    """
       Updates the given label with the provided result.
       """
    label.config(text=result)

def reset_label(label):
    """
        Resets the given label to its default text.
        """
    label.config(text=f"{label.cget('text').split(':')[0]}: ")

def show_error_message(message):
    """
       Displays an error message in a dialog box.
       """
    messagebox.showerror("Error", message)

def show_status_message(message):
    """
        Updates the status bar with the provided message.
        """
    status_var.set(message)
#Function to upload the file
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                file_data = file.read()
            process_file_data(file_data)
        except Exception as e:
            show_error_message(f"Error reading file: {e}")
#Function to process the uploaded file data
def process_file_data(file_data):
    try:
        # Split and strip the data
        raw_values = [item.strip() for item in file_data.replace('\n', ',').split(',') if item.strip()]

        # Convert to numeric values and validate
        values = []
        for item in raw_values:
            try:
                # Attempt to convert each item to a float
                numeric_value = float(item)
                values.append(numeric_value)
            except ValueError:
                # If conversion fails, raise an exception
                raise ValueError(f"Non-numeric data detected: '{item}'")

        update_data_display(values)
        show_status_message("File data uploaded.")
    except ValueError as e:
        show_error_message(str(e))
#Function for future use to save previous session data
def save_session_data():
    data = data_display.get('1.0', tk.END).strip()
    metrics = [label.cget("text") for label in stats_labels]
    with open('session_data.txt', 'w') as file:
        file.write(data + '\n' + '\n'.join(metrics))
#Function for future use to load previous session
def load_session_data():
    try:
        with open('session_data.txt', 'r') as file:
            lines = file.readlines()
        data = lines[0].strip()
        metrics = lines[1:]
        update_data_display(data.split(','))
        for label, metric in zip(stats_labels, metrics):
            label.config(text=metric.strip())
    except FileNotFoundError:
        pass  # No previous session data available
    except IndexError:
        pass  # Handle case where file format is not as expected

# Main application functions that perform calculations and manage the data

def generate_random_values():
    """
        Wrapper function to ask for number of values and trigger data generation.
        """
    ask_for_number_of_values()

def calculate_single_metric(metric_function, label):
    try:
        data = retrieve_data()
        metrics = Metricstics(data)
        result = metric_function(metrics)
        update_label_with_result(label, f"{metric_function.__name__.capitalize()}: {result}")
        # Removed the status bar update from here
    except ValueError as e:
        show_error_message(str(e))


def calculate_all_metrics():
    try:
        if not full_dataset:  # Check if the dataset is empty
            raise ValueError("No data to calculate metrics.")
        for metric_function, label in zip(stats_functions, stats_labels):
            threading.Thread(target=lambda: calculate_single_metric(metric_function[0], label), daemon=True).start()
        show_status_message("All metrics calculation started.")
    except ValueError as e:
        show_error_message(str(e))


def func_clear_all():
    """
       Clears all data from the data display and resets the labels to their default text.
       """
    global full_dataset
    full_dataset = []
    data_display.delete('1.0', tk.END)
    for label in stats_labels:
        reset_label(label)
    show_status_message("Data cleared.")

# GUI setup and layout

root = tk.Tk()
root.title('METRICSTICS')
root.geometry('800x600')

# Define styles for buttons, labels, and the data display area
button_style = {'font': ('Arial', 12), 'bg': '#D3D3D3', 'fg': 'black', 'padx': 10, 'pady': 5}
label_style = {'font': ('Arial', 12), 'bg': '#f0f0f0', 'fg': 'black'}
data_display_style = {'font': ('Consolas', 10), 'bg': '#fff', 'fg': 'black'}

# Create main frame to hold the content of the application
main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(expand=True, fill='both', padx=20, pady=20)

heading_label = tk.Label(main_frame, text="Welcome to METRICSTICS: A Statistical Calculator", **label_style)
heading_label.pack(pady=(0, 20))

# Data display where the generated or entered data will be shown
data_display = ScrolledText(main_frame, height=10, width=70, **data_display_style)
data_display.pack(pady=(0, 20))

# Buttons frame to hold action buttons
buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
buttons_frame.pack(pady=(0, 10))

# Generate button to trigger data generation
generate_button = tk.Button(buttons_frame, text='Generate Data', command=generate_random_values, **button_style)
generate_button.pack(side=tk.LEFT, padx=5)

# Calculate all button to compute all metrics for the data
calculate_all_button = tk.Button(buttons_frame, text='Calculate All Metrics', command=calculate_all_metrics, **button_style)
calculate_all_button.pack(side=tk.LEFT, padx=5)

# Clear button to clear the data and reset the application state
clear_all_button = tk.Button(buttons_frame, text='Clear All', command=func_clear_all, **button_style)
clear_all_button.pack(side=tk.LEFT, padx=5)

upload_file_button = tk.Button(buttons_frame, text='Upload File', command=upload_file, **button_style)
upload_file_button.pack(side=tk.LEFT, padx=5)

# Metrics frame to display the results of metric calculations
metrics_frame = tk.Frame(main_frame, bg='#f0f0f0')
metrics_frame.pack(fill='x', expand=True)

# Create labels and buttons for each metric defined in the stats_functions list
stats_labels = []
stats_functions = [
    (Metricstics.minimum, "Minimum"),
    (Metricstics.maximum, "Maximum"),
    (Metricstics.mode, "Mode"),
    (Metricstics.median, "Median"),
    (Metricstics.mean, "Mean"),
    (Metricstics.mean_absolute_deviation, "Mean Absolute Deviation"),
    (Metricstics.standard_deviation, "Standard Deviation"),
]

for i, (func, name) in enumerate(stats_functions):
    label = tk.Label(metrics_frame, text=f"{name}: ", **label_style)
    label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
    stats_labels.append(label)
    button = tk.Button(metrics_frame, text=f"Calculate {name}",
                       command=lambda f=func, l=label: calculate_single_metric(f, l), **button_style)
    button.grid(row=i, column=1, sticky='e', padx=5, pady=2)
# Status bar to display messages about the current application status
status_var = tk.StringVar(root)
status_bar = tk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor='w')
status_bar.pack(side=tk.BOTTOM, fill=tk.X)
show_status_message("Ready")
# Footer setup

footer_frame = tk.Frame(root, bg='#ddd', height=50)  # Increase the height for a bigger footer
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)  # Pack to the bottom of the window
footer_frame.pack_propagate(False)  # Prevent the frame from shrinking to fit its contents
footer_label = tk.Label(footer_frame, text="By Team N", font=('Arial', 14), bg='#ddd', fg='black')
footer_label.pack(pady=10)  # Increase the padding for a bigger label and center it vertically



root.mainloop()
