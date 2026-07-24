import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

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

pm_data.to_csv("philip_morris_pm_data.csv", index=False)

print(cross_MA[["Date", "Position", "Indicator_Type"]])

# фунція купівлі-продажу
def simulate_trading(data):
    money = float(input("Введіть суму інвестиції ($): "))
    cash = money
    shares = 0
    trades = []

    for index, row in cross_MA.iterrows():
        price = row["Close"]
        date = row["Date"]
        position = row["Position"]

        if position == 1 and cash > 0:
            shares = cash // price
            cash = 0
            trades.append({
                "Date": date,
                "Action": "BUY",
                "Price": round(price, 2),
                "Shares": round(shares, 4),
                "Cash": round(cash, 2)
            })
        elif position == -1 and shares > 0:
            cash = shares * price
            profit = cash - money
            trades.append({
                "Date": date,
                "Action": "SELL",
                "Price": round(price, 2),
                "Shares": round(shares, 4),
                "Cash": round(cash, 2),
                "Profit": round(profit, 2)
            })
            shares = 0
    if shares > 0:
        last_price = cross_MA.iloc[-1]["Close"]
        last_date = cross_MA.iloc[-1]["Date"]
        cash = shares * last_price
        profit = cash - money
        trades.append({
            "Date": last_date,
            "Action": "SELL (End)",
            "Price": round(last_price, 2),
            "Shares": round(shares, 4),
            "Cash": round(cash, 2),
            "Profit": round(profit, 2)
        })

    trades_df = pd.DataFrame(trades)

    print("\nІсторія угод")
    print(trades_df)

    print(f"Початкова сума: {money}")
    print(f"Кінцева сума: {round(cash, 2)}")
    print(f"Прибуток: {round(cash - money, 2)}")

    return trades_df

print(simulate_trading(pm_data))

plt.figure(figsize=(14, 7))
# Ціна закриття
plt.plot(pm_data["Date"], pm_data["Close"], label="Close Price", color="black")
# Ковзні середні
plt.plot(pm_data["Date"], pm_data["fast MA"],label="Fast MA (20)", color="blue")
plt.plot(pm_data["Date"], pm_data["slow MA"],label="Slow MA (50)", color="orange")
buy = pm_data[pm_data["Position"] == 1]
plt.scatter(
    buy["Date"],
    buy["Close"],
    color="green",
    marker="^",
    s=120,
    label="BUY"
)
# Точки продажу
sell = pm_data[pm_data["Position"] == -1]
plt.scatter(
    sell["Date"],
    sell["Close"],
    color="red",
    marker="v",
    s=120,
    label="SELL"
)
plt.title("Philip Morris (PM) Trading Signals")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
