import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

data = yf.download("PM", period="6mo")
data.to_csv("philis_morris_stock.csv")

plt.figure(figsize=(10,5))
plt.plot(data.index, data["Close"])
plt.title("PMI Stock Price")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.grid(True)
plt.show()