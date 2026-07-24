import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# створення си ес ви
data = yf.download("PM", start="2020-01-01", end="2020-12-31", auto_adjust=True)
try:
    data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
    data["Close"] = data["Close"].ffill()
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print("clearing data failed",e)


data.to_csv("philis_morris_stock.csv")

# фунція купівлі-продажу
def simulate_trading(data):
    money = float(input("Введіть суму інвестиції ($): "))
    cash = money
    shares = 0
    trades = []

    for row in data.iterrows():
        signal = row["Indicator_Type"]
        price = row["Close"]
        date = row["Date"]
        if signal == "Golden Cross (BUY)" and cash > 0:
            shares = cash // price
            cash = 0
            trades.append({
                "Date": date,
                "Action": "BUY",
                "Price": round(price, 2),
                "Shares": round(shares, 4),
                "Cash": round(cash, 2)
            })
        elif signal == "Death Cross (SELL)" and shares > 0:
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
        last_price = data.iloc[-1]["Close"]
        last_date = data.iloc[-1]["Date"]
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

    print(f"Купівля: {buy_price:.2f}$")
    print(f"Продаж: {sell_price:.2f}$")
    print(f"Прибуток: {profit:.2f}$")

    return trades_df


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
