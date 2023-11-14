import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText
from metricstics import Metricstics
import random

def ask_for_number_of_values():
    try:
        return simpledialog.askinteger("Input", "How many values would you like to generate?", minvalue=1, maxvalue=10000)
    except Exception as e:
        messagebox.showerror("Input Error", str(e))
        return None

def update_data_display(values):
    data_display.delete('1.0', tk.END)
    data_display.insert(tk.END, ', '.join(map(str, values)))

def retrieve_data():
    data_str = data_display.get('1.0', tk.END).strip()
    if not data_str:
        raise ValueError("No data generated.")
    
    data_list = data_str.split(',')
    data = []
    for item in data_list:
        try:
            num = int(item.strip())
            data.append(num)
        except ValueError:
            raise ValueError("Not a numerical value")
    return data

def update_label_with_result(label, result):
    label.config(text=result)

def reset_label(label):
    label.config(text=f"{label.cget('text').split(':')[0]}: ")

def show_error_message(message):
    messagebox.showerror("Error", message)

def validate_numeric_data(data):
    for value in data:
        if not isinstance(value, (int, float)):
            raise ValueError("Not a numerical value")

def generate_random_values():
    numeric_val = ask_for_number_of_values()
    if numeric_val is not None:
        try:
            val = [random.randint(0, 1000) for _ in range(numeric_val)]
            validate_numeric_data(val)
            update_data_display(val)
        except ValueError as e:
            show_error_message(str(e))

def calculate_single_metric(metric_function, label):
    try:
        data = retrieve_data()
        metrics = Metricstics(data)
        result = metric_function(metrics)
        update_label_with_result(label, f"{metric_function.__name__.capitalize()}: {result}")
    except ValueError as e:
        show_error_message(str(e))

def calculate_all_metrics():
    try:
        data = retrieve_data()
        for metric_function, label in zip(stats_functions, stats_labels):
            calculate_single_metric(metric_function[0], label)
    except ValueError as e:
        show_error_message(str(e))

def func_clear_all():
    data_display.delete('1.0', tk.END)
    for label in stats_labels:
        reset_label(label)

root = tk.Tk()
root.title('METRICSTICS')
root.geometry('800x600')

button_style = {
    'font': ('Arial', 12), 'bg': '#D3D3D3', 'fg': 'black', 'padx': 10, 'pady': 5
}
label_style = {
    'font': ('Arial', 12), 'bg': '#f0f0f0', 'fg': 'black'
}
data_display_style = {
    'font': ('Consolas', 10), 'bg': '#fff', 'fg': 'black'
}

main_frame = tk.Frame(root, bg='#f0f0f0')
main_frame.pack(expand=True, fill='both', padx=20, pady=20)

heading_label = tk.Label(main_frame, text="Welcome to METRICSTICS: A Statistical Calculator", **label_style)
heading_label.pack(pady=(0, 20))

data_display = ScrolledText(main_frame, height=10, width=70, **data_display_style)
data_display.pack(pady=(0, 20))

buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
buttons_frame.pack(pady=(0, 10))

generate_button = tk.Button(buttons_frame, text='Generate Data', command=generate_random_values, **button_style)
generate_button.pack(side=tk.LEFT, padx=5)

calculate_all_button = tk.Button(buttons_frame, text='Calculate All Metrics', command=calculate_all_metrics, **button_style)
calculate_all_button.pack(side=tk.LEFT, padx=(5, 20))  # Added padding for visual separation

clear_all_button = tk.Button(buttons_frame, text='Clear All', command=func_clear_all, **button_style)
clear_all_button.pack(side=tk.LEFT, padx=5)

metrics_frame = tk.Frame(main_frame, bg='#f0f0f0')
metrics_frame.pack(fill='x', expand=True)

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

footer_frame = tk.Frame(root, bg='#ddd', height=30)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
footer_frame.pack_propagate(False)

footer_label = tk.Label(footer_frame, text="By Team N", font=('Arial', 10), bg='#ddd', fg='black')
footer_label.pack()

root.mainloop()
