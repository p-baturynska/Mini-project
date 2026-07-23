import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Завантажуємо через об'єкт Ticker (ідеально працює з reset_index())
pm_ticker = yf.Ticker("PM")
pm_data = pm_ticker.history(start="2023-01-01", end="2024-01-01")

# Робимо дату звичайним стовпчиком
pm_data = pm_data.reset_index()

# Записуємо у файл
csv_data = pm_data.to_csv(index=False)

with open("philip_morris_pm_data.csv", mode="w", encoding="utf-8") as file:
    file.write(csv_data)