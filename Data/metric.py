import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

# Загрузка данных
data = pd.read_excel("train.xlsx", parse_dates=["dt"], index_col="dt")
data.columns = ["price"]
data = data.asfreq('W').ffill()

# Создание признаков
def create_features(df):
    features = df.copy()
    for lag in [1, 2, 3, 4, 8, 12]:
        features[f'lag_{lag}'] = features['price'].shift(lag)
    features['rolling_mean'] = features['price'].rolling(4).mean()
    features['rolling_std'] = features['price'].rolling(12).std()
    features['month'] = features.index.month
    return features.dropna()

processed_data = create_features(data)

# Обучение модели
X = processed_data.drop('price', axis=1)
y = processed_data['price']
model = XGBRegressor(n_estimators=500, learning_rate=0.01, max_depth=4, random_state=42)
model.fit(X, y)

# Функция прогнозирования
def forecast_price(last_data, weeks):
    forecast = []
    current_data = last_data.copy()
    
    for _ in range(weeks):
        next_row = {}
        for lag in [1, 2, 3, 4, 8, 12]:
            next_row[f'lag_{lag}'] = current_data['price'].shift(lag-1).iloc[-1]
        next_row['rolling_mean'] = current_data['price'].rolling(4).mean().iloc[-1]
        next_row['rolling_std'] = current_data['price'].rolling(12).std().iloc[-1]
        next_row['month'] = (current_data.index[-1] + pd.Timedelta(weeks=1)).month
        
        pred = model.predict(pd.DataFrame([next_row]))[0]
        forecast.append(pred)
        
        new_index = current_data.index[-1] + pd.Timedelta(weeks=1)
        current_data.loc[new_index] = [pred] + [np.nan]*(len(current_data.columns)-1)
        current_data = current_data.fillna(method='ffill')
    
    return forecast

# Создание GUI
class PriceForecastApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ цен на арматуру")
        self.root.geometry("1000x800")
        
        # Основные параметры
        self.weeks_to_forecast = 10
        self.show_past_weeks = 10
        
        # Создание интерфейса
        self.create_widgets()
        self.update_plot()
        
    def create_widgets(self):
        # Фрейм управления
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Выбор количества недель прогноза
        ttk.Label(control_frame, text="Недель прогноза:").grid(row=0, column=0, sticky=tk.W)
        self.weeks_slider = ttk.Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL, 
                                     command=lambda e: self.slider_changed())
        self.weeks_slider.set(10)
        self.weeks_slider.grid(row=0, column=1, sticky=tk.EW, padx=10)
        
        self.weeks_label = ttk.Label(control_frame, text="10 недель")
        self.weeks_label.grid(row=0, column=2, sticky=tk.W)
        
        # Кнопки быстрого выбора
        ttk.Button(control_frame, text="6 недель", command=lambda: self.set_weeks(6)).grid(row=1, column=0, pady=5)
        ttk.Button(control_frame, text="10 недель", command=lambda: self.set_weeks(10)).grid(row=1, column=1, pady=5)
        ttk.Button(control_frame, text="16 недель", command=lambda: self.set_weeks(16)).grid(row=1, column=2, pady=5)
        
        # Выбор исторического периода
        ttk.Label(control_frame, text="Показать прошлых недель:").grid(row=2, column=0, sticky=tk.W)
        self.past_weeks = ttk.Combobox(control_frame, values=[5, 10, 15, 20, 30, 50], width=5)
        self.past_weeks.set(10)
        self.past_weeks.grid(row=2, column=1, sticky=tk.W, padx=10)
        self.past_weeks.bind("<<ComboboxSelected>>", lambda e: self.update_plot())
        
        # Фрейм графика
        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создание графика
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Фрейм рекомендаций
        advice_frame = ttk.Frame(self.root, padding="10")
        advice_frame.pack(fill=tk.X)
        
        self.advice_text = tk.Text(advice_frame, height=8, wrap=tk.WORD, font=('Arial', 10))
        self.advice_text.pack(fill=tk.BOTH, expand=True)
        self.advice_text.tag_config('good', foreground='green')
        self.advice_text.tag_config('bad', foreground='red')
        
    def set_weeks(self, weeks):
        self.weeks_slider.set(weeks)
        self.weeks_label.config(text=f"{weeks} недель")
        self.update_plot()
        
    def slider_changed(self):
        weeks = int(self.weeks_slider.get())
        self.weeks_label.config(text=f"{weeks} недель")
        self.update_plot()
        
    def update_plot(self):
        # Получение параметров
        forecast_weeks = int(self.weeks_slider.get())
        past_weeks = int(self.past_weeks.get())
        
        # Подготовка данных
        last_date = data.index[-1]
        last_data = data.tail(12)
        
        # Прогнозирование
        forecast_values = forecast_price(last_data, forecast_weeks)
        future_dates = pd.date_range(last_date, periods=forecast_weeks+1, freq='W')[1:]
        
        # Очистка графика
        self.ax.clear()
        
        # Построение исторических данных
        history_start = max(0, len(data) - past_weeks)
        self.ax.plot(data.index[history_start:], data['price'][history_start:], 
                   label='История', color='blue', lw=2)
        
        # Построение прогноза
        self.ax.plot(future_dates, forecast_values, 'r--', label='Прогноз', lw=2)
        
        # Текущая точка
        self.ax.scatter([last_date], [data['price'][-1]], color='red', s=100, label='Текущая цена')
        
        # Настройки графика
        self.ax.set_title(f'Прогноз цены на арматуру на {forecast_weeks} недель')
        self.ax.set_xlabel('Дата')
        self.ax.set_ylabel('Цена')
        self.ax.grid(True)
        self.ax.legend()
        
        # Автомасштабирование
        min_y = min(data['price'][history_start:].min(), min(forecast_values))
        max_y = max(data['price'][history_start:].max(), max(forecast_values))
        self.ax.set_ylim(min_y * 0.95, max_y * 1.05)
        
        # Обновление холста
        self.canvas.draw()
        
        # Генерация рекомендаций
        self.generate_advice(forecast_values, forecast_weeks)
        
    def generate_advice(self, forecast, weeks):
        current_price = data['price'][-1]
        min_price = min(forecast)
        max_price = max(forecast)
        final_price = forecast[-1]
        
        # Очистка текста
        self.advice_text.delete(1.0, tk.END)
        
        # Основная информация
        self.advice_text.insert(tk.END, 
                              f"Текущая цена: {current_price:.2f}\n"
                              f"Прогноз через {weeks} недель: {final_price:.2f}\n"
                              f"Минимальная цена в прогнозе: {min_price:.2f}\n"
                              f"Максимальная цена в прогнозе: {max_price:.2f}\n\n")
        
        # Анализ для 6 недель
        if weeks >= 6:
            six_week_price = forecast[5]
            change_6weeks = (six_week_price - current_price) / current_price * 100
            
            self.advice_text.insert(tk.END, f"Через 6 недель: {six_week_price:.2f} ({change_6weeks:+.1f}%)\n")
            
            if six_week_price < current_price:
                self.advice_text.insert(tk.END, "→ Цена снизится через 6 недель\n", 'bad')
            else:
                self.advice_text.insert(tk.END, "→ Цена вырастет через 6 недель\n", 'good')
        
        # Анализ для 10 недель
        if weeks >= 10:
            ten_week_price = forecast[9]
            change_10weeks = (ten_week_price - current_price) / current_price * 100
            
            self.advice_text.insert(tk.END, f"\nЧерез 10 недель: {ten_week_price:.2f} ({change_10weeks:+.1f}%)\n")
            
            if ten_week_price < current_price:
                self.advice_text.insert(tk.END, "→ Цена снизится через 10 недель\n", 'bad')
            else:
                self.advice_text.insert(tk.END, "→ Цена вырастет через 10 недель\n", 'good')
        
        # Общая рекомендация
        self.advice_text.insert(tk.END, "\nОбщая рекомендация:\n")
        
        if min_price < current_price * 0.98:  # Если будет снижение более 2%
            self.advice_text.insert(tk.END, 
                                  "Подождите с закупкой!\n"
                                  f"Ожидается снижение цены до {min_price:.2f} "
                                  f"({(min_price-current_price)/current_price*100:.1f}%)\n"
                                  "Лучшее время для закупки через "
                                  f"{forecast.index(min_price)+1} недель(ю).", 'bad')
        else:
            self.advice_text.insert(tk.END, 
                                  "Закупайтесь сейчас!\n"
                                  "Цена будет расти или останется стабильной.\n"
                                  "Минимальная прогнозируемая цена: "
                                  f"{min_price:.2f} ({min_price-current_price:+.1f})", 'good')

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PriceForecastApp(root)
    root.mainloop()