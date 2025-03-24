



# import tkinter as tk
# import matplotlib as mlt
# from tkinter import ttk
# from PIL import Image, ImageTk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np


# def close_window():
#     window.destroy()


# def start_move(event):
#     global start_x, start_y
#     start_x = event.x
#     start_y = event.y

# def move(event):
#     x = window.winfo_x() + event.x - start_x
#     y = window.winfo_y() + event.y - start_y
#     window.geometry(f"+{x}+{y}")

# def on_date_selected(event):
#     selected_date = date_combobox.get()
#     result_label.config(text=f"Вы выбрали: {selected_date}")
#     draw_graph(selected_date)


# def draw_graph(date):
#     x = np.arange(1, 11)
#     y = np.random.rand(10) * 10

#     for widget in graph_frame.winfo_children():
#         widget.destroy()

#     fig, ax = plt.subplots(figsize=(5, 3))
#     ax.plot(x, y, marker='o', color='orange', linewidth=2)
#     ax.set_title(f"Прогноз для {date}")
#     ax.set_xlabel("Период")
#     ax.set_ylabel("Значение")

#     canvas = FigureCanvasTkAgg(fig, master=graph_frame)
#     canvas.draw()
#     canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# window = tk.Tk()
# window.overrideredirect(True)
# window.minsize(1000, 700)


# title_bar = tk.Frame(window, bg='#9EE7AF')
# title_bar.pack(side="top", fill="x")

# dates = [
#     "2022-09-05 - 2022-09-12", "2022-09-12 - 2022-09-19", "2022-09-19 - 2022-09-26",
#     "2022-09-26 - 2022-10-03", "2022-10-03 - 2022-10-10", "2022-10-10 - 2022-10-17",
#     "2022-10-17 - 2022-10-24", "2022-10-24 - 2022-10-31", "2022-10-31 - 2022-11-07",
#     "2022-11-07 - 2022-11-14", "2022-11-14 - 2022-11-21", "2022-11-21 - 2022-11-28",
#     "2022-11-28 - 2022-12-05", "2022-12-05 - 2022-12-12", "2022-12-12 - 2022-12-19",
#     "2022-12-19 - 2022-12-26", "2022-12-26 - 2023-01-02", "2023-01-02 - 2023-01-09",
#     "2023-01-09 - 2023-01-16", "2023-01-16 - 2023-01-23", "2023-01-23 - 2023-01-30",
#     "2023-01-30 - 2023-02-06", "2023-02-06 - 2023-02-13", "2023-02-13 - 2023-02-20",
#     "2023-02-20 - 2023-02-27", "2023-02-27 - 2023-03-06"
# ]

# custom_font = ("Arial", 10)
# date_combobox = ttk.Combobox(window, values=dates, width=22, font=custom_font)
# date_combobox.set("Выберите дату")
# date_combobox.place(x=750, y=30)


# result_frame = tk.Frame(window, bg="#DFF6FF", width=400, height=100, relief="groove", borderwidth=2)
# result_frame.place(x=750, y=90)

# result_label = tk.Label(result_frame, text="Здесь будет результат", font=("Arial", 14), fg="blue", bg="#DFF6FF")
# result_label.pack(expand=True, fill="both")

# graph_frame = tk.Frame(window, bg="#FFFFFF", width=500, height=500, relief="sunken", borderwidth=2)
# graph_frame.place(x=30, y=10)

# date_combobox.bind("<<ComboboxSelected>>", on_date_selected)


# title_bar.bind("<Button-1>", start_move)
# title_bar.bind("<B1-Motion>", move)


# title_label = tk.Label(title_bar, text="Predskazanie", bg='#9EE7AF', font=("Arial", 14))
# title_label.pack(side="left", padx=10)


# exit_image = Image.open("exit.png")
# exit_image = exit_image.resize((20, 20))
# exit_photo = ImageTk.PhotoImage(exit_image)

# exit_button = tk.Button(title_bar, image=exit_photo, command=close_window, bg='#9EE7AF', bd=0)
# exit_button.pack(side="right", padx=10)


# window.mainloop()


import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def predict_price():
    selected_date = date_entry.get()
    quantity = quantity_entry.get()
    
    # Пример предсказания — заменить на реальную модель
    future_prices = [100 + i * 2 for i in range(30)]
    past_prices = [100 - i * 2 for i in range(6)][::-1]
    
    if future_prices[0] > past_prices[-1]:
        recommendation = "Покупать"
    elif future_prices[0] < past_prices[-1]:
        recommendation = "Не покупать"
    else:
        recommendation = "Изменение цены не ожидается"

    recommendation_label.config(text=f"Рекомендация: {recommendation}")
    
    # Построение графика
    plt.clf()
    weeks_past = [f"- {i+1}" for i in range(6)][::-1]
    weeks_future = [f"+ {i+1}" for i in range(30)]
    weeks = weeks_past + ["Текущая неделя"] + weeks_future
    prices = past_prices + [past_prices[-1]] + future_prices
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(weeks, prices, marker='o', color='blue')
    ax.set_title('История и прогноз цен на арматуру')
    ax.set_xlabel('Недели')
    ax.set_ylabel('Цена')
    ax.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def save_to_excel():
    selected_date = date_entry.get()
    quantity = quantity_entry.get()
    if not selected_date or not quantity:
        messagebox.showwarning("Ошибка", "Введите дату и количество!")
        return
    
    data = {'Дата': [selected_date], 'Количество арматуры': [quantity]}
    df = pd.DataFrame(data)
    df.to_excel('invoice.xlsx', index=False)
    messagebox.showinfo("Успех", "Накладная сохранена в invoice.xlsx")

# Интерфейс
window = tk.Tk()
window.title('Приложение для категорийного менеджера')
window.geometry('800x600')

frame = tk.Frame(window)
frame.pack(pady=10)

# Ввод даты
date_label = tk.Label(frame, text='Введите дату (ГГГГ-ММ-ДД):')
date_label.grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=1, padx=5, pady=5)

# Ввод количества
quantity_label = tk.Label(frame, text='Введите количество арматуры:')
quantity_label.grid(row=1, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(frame)
quantity_entry.grid(row=1, column=1, padx=5, pady=5)

# Кнопка предсказания
predict_button = tk.Button(frame, text='Получить прогноз', command=predict_price)
predict_button.grid(row=2, column=0, columnspan=2, pady=10)

# Рекомендация
recommendation_label = tk.Label(window, text='Рекомендация: —', font=('Arial', 14))
recommendation_label.pack(pady=10)

# Кнопка сохранения накладной
save_button = tk.Button(window, text='Сохранить накладную в Excel', command=save_to_excel)
save_button.pack(pady=10)

window.mainloop()
