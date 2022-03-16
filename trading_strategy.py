# IMPORT THE REQUIRED LIBRARIES
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


GDAXI = yf.download(

    tickers='^GDAXI',   # The DAX is a stock market index consisting of the 40 major German blue chip companies
    start='2022-01-01',  # This line ensures only the stock data as from 2022-01-01 is downloaded
    threads=True,  # Using multithreading to reduce the time complexity of the program
)

# CREATE A SIMPLE MOVING AVERAGE WITH A 2 DAY WINDOW - SHORT TERM AVERAGE
SMA2 = pd.DataFrame() # We first create a new data frame
SMA2['Adj. Close Price'] = GDAXI['Adj Close'].rolling(window=2).mean()
# Dropping the null values
SMA2 = SMA2.dropna()


# CREATE A SIMPLE MOVING AVERAGE WITH A 10 DAY WINDOW - LONG TERM AVERAGE
SMA10 = pd.DataFrame()  # # We first create a new data frame
SMA10['Adj. Close Price'] = GDAXI['Adj Close'].rolling(window=10).mean()
# Dropping the null values
SMA10 = SMA10.dropna()

# Creating a new data frame
data = pd.DataFrame()
data['Adj. Close'] = GDAXI['Adj Close']
data['SMA2'] = SMA2['Adj. Close Price']
data['SMA10'] = SMA10['Adj. Close Price']
# Drop the null values
data = data.dropna()


# Creating a function to signal when to buy or sell the asset/stock
def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data['SMA2'][i] > data['SMA10'][i]:
            if flag != 1:
                sigPriceBuy.append(data['Adj. Close'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA2'][i] < data['SMA10'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['Adj. Close'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy, sigPriceSell)


# Store the buy and sell data into a variable
buy_sell = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]

# Visualize the data and strategy to buy and sell the stock
plt.figure(figsize=(20, 8))
plt.plot(data['Adj. Close'], label='Adj Close', alpha=0.90)
plt.plot(data['SMA2'], label='SMA2', alpha=0.90)
plt.plot(data['SMA10'], label='SMA10', alpha=0.90)
plt.scatter(data.index, data['Buy_Signal_Price'], label='Buy', marker='^', color='green')
plt.scatter(data.index, data['Sell_Signal_Price'], label='Sell', marker='v', color='red')
plt.grid()
plt.title('GDAXI Adjusted Close Price History Buy & Sell Signals')
plt.xlabel('Jan. 03, 2022 - Mar. 15, 2022')
plt.ylabel('Adj. Close Price USD($)')
plt.legend(loc='lower left')
plt.show()
