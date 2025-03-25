import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, r2_score
from statsmodels.tsa.seasonal import seasonal_decompose
from PIL import Image, ImageTk


# Функция для загрузки и предсказания с использованием модели SARIMAX
def load_and_forecast():
    # Загрузка данных
    df = pd.read_excel("train.xlsx")
    df.set_index("dt", inplace=True)

    # Обучение модели SARIMAX
    model = SARIMAX(df["Цена на арматуру"],
                    order=(1, 1, 1),  
                    seasonal_order=(1, 1, 1, 52),
                    enforce_stationarity=False, 
                    enforce_invertibility=False)
    sarimax_model = model.fit(disp=False)
    
    # Прогноз на 30 недель вперёд
    forecast_steps = 30
    forecast = sarimax_model.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(df.index[-1], periods=forecast_steps + 1, freq='W')[1:]

    forecast_mean = forecast.predicted_mean
    forecast_ci = forecast.conf_int()

    return forecast_index, forecast_mean, forecast_ci


# Функция для отображения графика
def draw_graph(date):
    # Получаем прогноз
    forecast_index, forecast_mean, forecast_ci = load_and_forecast()

    # Очистка предыдущего графика
    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(forecast_index, forecast_mean, label="Прогноз", color="red", linestyle="--", linewidth=2)
    ax.fill_between(forecast_index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='red', alpha=0.2)

    ax.set_title(f"Прогноз для {date}")
    ax.set_xlabel("Неделя")
    ax.set_ylabel("Цена")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Функция для анализа изменения тренда
def make_decision():
    forecast_index, forecast_mean, forecast_ci = load_and_forecast()
    
    # Для принятия решения проверим на рост или падение цены в будущем
    if forecast_mean.iloc[1] > forecast_mean.iloc[0]:  # сравниваем прогноз на следующие 2 недели
        decision_label.config(text="Рекомендуется купить!")
    else:
        decision_label.config(text="Рекомендуется не покупать!")


# Закрытие окна
def close_window():
    window.destroy()


# Перемещение окна
def start_move(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def move(event):
    x = window.winfo_x() + event.x - start_x
    y = window.winfo_y() + event.y - start_y
    window.geometry(f"+{x}+{y}")


window = tk.Tk()
window.overrideredirect(True)
window.minsize(1000, 700)

title_bar = tk.Frame(window, bg='#9EE7AF')
title_bar.pack(side="top", fill="x")

# Даты для комбобокса
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
result_frame.place(x=750, y=90)

result_label = tk.Label(result_frame, text="Здесь будет результат", font=("Arial", 14), fg="blue", bg="#DFF6FF")
result_label.pack(expand=True, fill="both")

graph_frame = tk.Frame(window, bg="#FFFFFF", width=600, height=600, relief="sunken", borderwidth=2)
graph_frame.place(x=50, y=40)

# Действия при выборе даты
date_combobox.bind("<<ComboboxSelected>>", lambda event: draw_graph(date_combobox.get()))

# Перетаскивание окна
title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", move)

title_label = tk.Label(title_bar, text="Predskazanie", bg='#9EE7AF', font=("Arial", 14))
title_label.pack(side="left", padx=10)

exit_image = Image.open("exit.png")
exit_image = exit_image.resize((20, 20))
exit_photo = ImageTk.PhotoImage(exit_image)

exit_button = tk.Button(title_bar, image=exit_photo, command=close_window, bg='#9EE7AF', bd=0)
exit_button.pack(side="right", padx=10)

# Кнопка для анализа рекомендации
decision_button = tk.Button(window, text="Проанализировать рекомендации", command=make_decision)
decision_button.place(x=750, y=200)

decision_label = tk.Label(window, text="Решение будет здесь", font=("Arial", 12), fg="red")
decision_label.place(x=750, y=250)

window.mainloop()
