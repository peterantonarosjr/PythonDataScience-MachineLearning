#Imports
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import cufflinks as cf
cf.go_offline()
print("Imports succesful")

#Import Bank Data
print("Grabbing data from Yahoo Finance")
start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)

# Bank of America
BAC = data.DataReader("BAC", 'yahoo', start, end)
# CitiGroup
C = data.DataReader("C", 'yahoo', start, end)
# Goldman Sachs
GS = data.DataReader("GS", 'yahoo', start, end)
# JPMorgan Chase
JPM = data.DataReader("JPM", 'yahoo', start, end)
# Morgan Stanley
MS = data.DataReader("MS", 'yahoo', start, end)
# Wells Fargo
WFC = data.DataReader("WFC", 'yahoo', start, end)

#Bank Tickers 
tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']
bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC],axis=1,keys=tickers)
bank_stocks.columns.names = ['Bank Ticker','Stock Info']

#Data Check
print(bank_stocks.tail(5))
print("Max closing price\n",bank_stocks.xs(key='Close',axis=1,level='Stock Info').max())

#Returns DataFrame of returns per bank per day
returns = pd.DataFrame()
for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()
print(returns.head())

sns.set(style="ticks", color_codes=True)
r_pair = sns.pairplot(data=returns[1:], height=1.5, aspect=1)


print("Worst day of returns")
print(returns.idxmin())
print("Best day of returns")
print(returns.idxmax())

print("Standard deviation of returns")
print(returns.std())

print("Standard deviation of returns 1/1/15-12/31/15")
print(returns.loc['2015-01-01':'2015-12-31'].std())

#Morgan Stanley 2015 returns
plt.figure()
sns.set(style="ticks", color_codes=True)
d_plot = sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS Return'], color='green',kde=True, bins=100)

#Citigroup 2008 returns
plt.figure()
sns.set(style="ticks", color_codes=True)
d_plot2 = sns.distplot(returns.loc['2008-01-01':'2008-12-31']['C Return'], color='red', kde=True, bins=100)
 
#Closing price for each bank over entire index of time
sns.set_style('whitegrid')
bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot(figsize=(12,4))
plt.tight_layout()

#Rolling average vs BAC closing in 2008
plt.figure(figsize=(12,6))
BAC['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].loc['2008-01-01':'2009-01-01'].plot(label='BAC CLOSE')
plt.legend()
plt.tight_layout()

#Correlation of closing price for each Bank
plt.figure()
h_map = sns.heatmap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True, cmap='magma', linewidths=0.35)
c_map = sns.clustermap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True, cmap='magma', linewidths=0.35, figsize=(10,7))

#Display
plt.show()