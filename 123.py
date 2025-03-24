



import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def close_window():
    window.destroy()


def start_move(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def move(event):
    x = window.winfo_x() + event.x - start_x
    y = window.winfo_y() + event.y - start_y
    window.geometry(f"+{x}+{y}")

def on_date_selected(event):
    selected_date = date_combobox.get()
    result_label.config(text=f"Вы выбрали: {selected_date}")
    draw_graph(selected_date)


def draw_graph(date):
    x = np.arange(1, 11)
    y = np.random.rand(10) * 10

    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, y, marker='o', color='orange', linewidth=2)
    ax.set_title(f"Прогноз для {date}")
    ax.set_xlabel("Период")
    ax.set_ylabel("Значение")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


window = tk.Tk()
window.overrideredirect(True)
window.minsize(1000, 700)


title_bar = tk.Frame(window, bg='#9EE7AF')
title_bar.pack(side="top", fill="x")

dates = [
    "2022-09-05 - 2022-09-12", "2022-09-12 - 2022-09-19", "2022-09-19 - 2022-09-26",
    "2022-09-26 - 2022-10-03", "2022-10-03 - 2022-10-10", "2022-10-10 - 2022-10-17",
    "2022-10-17 - 2022-10-24", "2022-10-24 - 2022-10-31", "2022-10-31 - 2022-11-07",
    "2022-11-07 - 2022-11-14", "2022-11-14 - 2022-11-21", "2022-11-21 - 2022-11-28",
    "2022-11-28 - 2022-12-05", "2022-12-05 - 2022-12-12", "2022-12-12 - 2022-12-19",
    "2022-12-19 - 2022-12-26", "2022-12-26 - 2023-01-02", "2023-01-02 - 2023-01-09",
    "2023-01-09 - 2023-01-16", "2023-01-16 - 2023-01-23", "2023-01-23 - 2023-01-30",
    "2023-01-30 - 2023-02-06", "2023-02-06 - 2023-02-13", "2023-02-13 - 2023-02-20",
    "2023-02-20 - 2023-02-27", "2023-02-27 - 2023-03-06"
]

custom_font = ("Arial", 10)
date_combobox = ttk.Combobox(window, values=dates, width=22, font=custom_font)
date_combobox.set("Выберите дату")
date_combobox.place(x=750, y=30)


result_frame = tk.Frame(window, bg="#DFF6FF", width=400, height=100, relief="groove", borderwidth=2)
result_frame.place(x=300, y=200)

result_label = tk.Label(result_frame, text="Здесь будет результат", font=("Arial", 14), fg="blue", bg="#DFF6FF")
result_label.pack(expand=True, fill="both")

graph_frame = tk.Frame(window, bg="#FFFFFF", width=400, height=300, relief="sunken", borderwidth=2)
graph_frame.place(x=300, y=350)

date_combobox.bind("<<ComboboxSelected>>", on_date_selected)


title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", move)


title_label = tk.Label(title_bar, text="Predskazanie", bg='#9EE7AF', font=("Arial", 14))
title_label.pack(side="left", padx=10)


exit_image = Image.open("exit.png")
exit_image = exit_image.resize((20, 20))
exit_photo = ImageTk.PhotoImage(exit_image)

exit_button = tk.Button(title_bar, image=exit_photo, command=close_window, bg='#9EE7AF', bd=0)
exit_button.pack(side="right", padx=10)


window.mainloop()
