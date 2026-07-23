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


# складно зробити без того що зробила полінка
money = float(input("Enter your money to invest: "))
def sell_buy(money):
    # for points in crosses:
        # buy_price = ??? перетин отих ковзанок
        # shares = money / buy_price
        # sell_price = ??? інший перетин
        # profit = shares * sell_price - money
#         зробити табличку виводу коли купувати/продавати


print(f"Купівля: {buy_price:.2f}$")
print(f"Продаж: {sell_price:.2f}$")
print(f"Прибуток: {profit:.2f}$")
# графік
# додати точки продажу\купівлі,
# додати 2 лінії якоїсь чортівні на основі коду іншої людини
plt.figure(figsize=(10,5))
plt.plot(data.index, data["Close"])
plt.title("PMI Stock Price")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.grid(True)
plt.show()