import yfinance as yf
import pandas as pd
# import matplotlib.pyplot as plt

pm_ticker = yf.Ticker("PM")

# Беремо початкову дату і віднімаємо 75 днів
start_dt = pd.to_datetime("2023-01-01") - pd.Timedelta(days=75)
start_date_str = start_dt.strftime("%Y-%m-%d")

# Завантажуємо дані з запасом
pm_data = pm_ticker.history(start=start_date_str, end="2024-01-01")
# Робимо дату звичайним стовпчиком
pm_data = pm_data.reset_index()

# Записуємо у файл
pm_data.to_csv("philip_morris_pm_data.csv", index=False)

# додали швидку ковзну та повільну
pm_data["fast MA"] = pm_data["Close"].rolling(window=20).mean()
pm_data["slow MA"] = pm_data["Close"].rolling(window=50).mean()

# 2. Відсікаємо буферний 2022 рік! Залишаємо тільки дані з 2023-01-01
pm_data = pm_data[pm_data["Date"] >= "2023-01-01"]

# 3. Скидаємо індекси, щоб вони знову йшли від 0 до N
pm_data = pm_data.reset_index(drop=True)

# створюємо нову колонку індикатор, де буде вказуватися чи швидка ковзка більша за повільну і повертати або True
# або False, а функція astype() перетворює булевий тип у число 0 або 1
pm_data["Indicator"]= (pm_data["fast MA"] >= pm_data["slow MA"]).astype(int)

# функція diff() бере значення в стовпці Індикатор віднімає від нього значення попереднього і повертає різницю
pm_data["Position"] = pm_data["Indicator"].diff()

# заповнюємо N/A в першому рядку на 0
pm_data["Position"] = pm_data["Position"].fillna(0)

# створюємо нову колонку. До колонки позишион приміняєм словничок, тепер колонка ідкитор тайп тепер людською мовою написана
pm_data["Indicator_Type"] = pm_data["Position"].map({
    1: "Golden Cross (BUY)",
    -1: "Death Cross (SELL)"
})
# створюємо новий df який є зрізиком із великої таблички. Він містить лише дата там де є зміна індикатора
cross_MA = pm_data[pm_data["Position"] != 0]

# па пріколу її надрукуєм
print(cross_MA[["Date", "Close", "fast MA", "slow MA","Position", "Indicator_Type"]])

pm_data.to_csv("philip_morris_pm_data.csv", index=False)

