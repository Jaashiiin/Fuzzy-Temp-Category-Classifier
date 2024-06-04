import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox


def get_temp(temp):
    freezing, cool, warm, hot = 0, 0, 0, 0

    if temp < 30:
        freezing = 100
    elif 30 <= temp < 50:
        freezing = (-0.05 * temp + 2.5) * 100
        cool = (0.05 * temp - 1.5) * 100
    elif 50 <= temp < 70:
        cool = (-0.05 * temp + 3.5) * 100
        warm = (0.05 * temp - 2.5) * 100
    elif 70 <= temp < 90:
        warm = (-0.05 * temp + 4.5) * 100
        hot = (0.05 * temp - 3.5) * 100
    else:
        hot = 100

    categories = {
        "Freezing": freezing / 100,
        "Cool": cool / 100,
        "Warm": warm / 100,
        "Hot": hot / 100
    }

    category = max(categories, key=categories.get)
    categories_percentage = {key: value * 100 for key, value in categories.items()}

    return category, categories_percentage


def show_result():
    try:
        temp = float(temp_entry.get())
        category, values = get_temp(temp)

        result_text_label.config(state=tk.NORMAL)
        result_text_label.delete(1.0, tk.END)
        result_text_label.insert(tk.END, "The temperature is classified as: ")

        if category == "Freezing":
            result_text_label.insert(tk.END, category, ("freezing",))
        elif category == "Cool":
            result_text_label.insert(tk.END, category, ("cool",))
        elif category == "Warm":
            result_text_label.insert(tk.END, category, ("warm",))
        else:
            result_text_label.insert(tk.END, category, ("hot",))

        result_text_label.tag_config("freezing", foreground="blue")
        result_text_label.tag_config("cool", foreground="cyan")
        result_text_label.tag_config("warm", foreground="orange")
        result_text_label.tag_config("hot", foreground="red")

        result_text.delete(1.0, tk.END)
        max_category_length = max(len(category) for category in values.keys())
        for key, value in values.items():
            padding = max_category_length - len(key)
            formatted_value = f"{value:.2f}%"
            result_text.insert(tk.END, f"{key}:{' ' * padding} {formatted_value}\n")

        categories = list(values.keys())
        membership_values = list(values.values())
        fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted size
        ax.bar(categories, membership_values, color=['blue', 'cyan', 'orange', 'red'])
        ax.set_xlabel('Temperature Categories')
        ax.set_ylabel('Membership Value (%)')
        ax.set_title('Temperature Category Membership Values')
        ax.set_ylim(0, 100)

        for widget in chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")


root = tk.Tk()
root.title("Temperature Category Classifier")

title_label = ttk.Label(root, text="Temperature Category Classifier", font=('Verdana', 18, 'bold'))
title_label.pack(pady=20)

mainframe = ttk.Frame(root, padding="10")
mainframe.pack(fill=tk.BOTH, expand=True)

ttk.Label(mainframe, text="Enter the temperature in °F:", font=('Verdana', 14)).grid(row=0, column=0, padx=5, pady=5,
                                                                                     sticky='W')
temp_entry = ttk.Entry(mainframe, width=16, font=('Verdana', 14))
temp_entry.grid(row=0, column=1, padx=5, pady=5, sticky='W')

button_style = ttk.Style()
button_style.configure("Custom.TButton", font=('Verdana', 12))
show_button = ttk.Button(mainframe, text="Show Result", command=show_result, style="Custom.TButton")
show_button.grid(row=0, column=2, padx=10, pady=10, sticky='W')

result_text_label = tk.Text(mainframe, width=34, height=1, font=('Verdana', 14, 'bold'), state=tk.DISABLED)
result_text_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='W')

result_text = tk.Text(mainframe, width=40, height=10, font=('Verdana', 14))
result_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='W')

chart_frame = ttk.Frame(mainframe)
chart_frame.grid(row=0, column=3, rowspan=3, padx=5, pady=5, sticky='N')

root.mainloop()
